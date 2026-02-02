import os
from requests_oauthlib import OAuth2Session

FITBIT_AUTH_BASE = 'https://www.fitbit.com/oauth2/authorize'
FITBIT_TOKEN_URL = 'https://api.fitbit.com/oauth2/token'

def make_fitbit_session(client_id, redirect_uri, scope=None, token=None):
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope, token=token)
