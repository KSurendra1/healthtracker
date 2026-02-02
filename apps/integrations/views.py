import os
import time
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from requests_oauthlib import OAuth2Session
from google_auth_oauthlib.flow import Flow
from .models import ExternalAccount


@login_required
def oauth_connect(request, provider):
    redirect_uri = request.build_absolute_uri(reverse('oauth-callback', args=[provider]))

    if provider == 'fitbit':
        client_id = os.getenv('FITBIT_CLIENT_ID', '')
        scope = ['activity', 'heartrate', 'sleep']
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        authorization_url, state = oauth.authorization_url('https://www.fitbit.com/oauth2/authorize')
        request.session['oauth_state'] = state
        return redirect(authorization_url)

    if provider == 'googlefit':
        client_id = os.getenv('GOOGLE_CLIENT_ID', '')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')
        scopes = [
            'https://www.googleapis.com/auth/fitness.activity.read',
            'https://www.googleapis.com/auth/fitness.body.read',
            'openid',
            'email',
        ]
        client_config = {
            'web': {
                'client_id': client_id,
                'client_secret': client_secret,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
            }
        }
        flow = Flow.from_client_config(client_config, scopes=scopes, redirect_uri=redirect_uri)
        auth_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true', prompt='consent')
        request.session['oauth_state'] = state
        return redirect(auth_url)

    return redirect('/')


class ProvidersListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        providers = [
            {
                'key': 'fitbit',
                'name': 'Fitbit',
                'connect_url': request.build_absolute_uri(reverse('oauth-connect', args=['fitbit'])),
            },
            {
                'key': 'googlefit',
                'name': 'Google Fit',
                'connect_url': request.build_absolute_uri(reverse('oauth-connect', args=['googlefit'])),
            },
        ]
        return Response(providers)


@login_required
def oauth_callback(request, provider):
    redirect_uri = request.build_absolute_uri(reverse('oauth-callback', args=[provider]))

    if provider == 'fitbit':
        client_id = os.getenv('FITBIT_CLIENT_ID', '')
        client_secret = os.getenv('FITBIT_CLIENT_SECRET', '')
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, state=request.session.get('oauth_state'))
        token = oauth.fetch_token(
            'https://api.fitbit.com/oauth2/token',
            client_secret=client_secret,
            authorization_response=request.build_absolute_uri(),
        )
        expires_at = None
        if 'expires_at' in token:
            try:
                expires_at = timezone.datetime.fromtimestamp(int(token['expires_at']), tz=timezone.utc)
            except Exception:
                expires_at = None

        ExternalAccount.objects.update_or_create(
            user=request.user,
            provider='fitbit',
            defaults={
                'provider_user_id': token.get('user_id', ''),
                'access_token': token.get('access_token', ''),
                'refresh_token': token.get('refresh_token', ''),
                'expires_at': expires_at,
            }
        )
        # Optionally trigger background sync task
        try:
            from .tasks import trigger_initial_sync
            trigger_initial_sync.delay(request.user.id, 'fitbit')
        except Exception:
            pass
        return redirect('/')

    if provider == 'googlefit':
        client_id = os.getenv('GOOGLE_CLIENT_ID', '')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')
        client_config = {
            'web': {
                'client_id': client_id,
                'client_secret': client_secret,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
            }
        }
        flow = Flow.from_client_config(client_config, scopes=None, redirect_uri=redirect_uri)
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        expires_at = None
        if hasattr(credentials, 'expiry') and credentials.expiry:
            expires_at = credentials.expiry

        ExternalAccount.objects.update_or_create(
            user=request.user,
            provider='googlefit',
            defaults={
                'provider_user_id': getattr(credentials, 'id_token', '') or '',
                'access_token': credentials.token,
                'refresh_token': getattr(credentials, 'refresh_token', ''),
                'expires_at': expires_at,
            }
        )
        try:
            from .tasks import trigger_initial_sync
            trigger_initial_sync.delay(request.user.id, 'googlefit')
        except Exception:
            pass
        return redirect('/')

    return redirect('/')
