import os
import base64
import logging
import requests

logger = logging.getLogger(__name__)


def revoke_external_account_tokens(account):
    """Attempt to revoke tokens for the given ExternalAccount.

    Returns True if revocation was attempted (and likely succeeded), False otherwise.
    """
    provider = account.provider
    token = getattr(account, 'refresh_token', None) or getattr(account, 'access_token', None)
    if not token:
        logger.debug('No token to revoke for account %s', account)
        return False

    try:
        if provider == 'fitbit':
            client_id = os.getenv('FITBIT_CLIENT_ID', '')
            client_secret = os.getenv('FITBIT_CLIENT_SECRET', '')
            creds = f"{client_id}:{client_secret}".encode('utf-8')
            auth = base64.b64encode(creds).decode('utf-8')
            headers = {
                'Authorization': f'Basic {auth}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {'token': token}
            resp = requests.post('https://api.fitbit.com/oauth2/revoke', headers=headers, data=data, timeout=10)
            logger.info('Fitbit revoke response %s for account %s', resp.status_code, account)
            return resp.status_code in (200, 204)

        if provider == 'googlefit':
            # Prefer revoking the refresh token when available, otherwise fallback to access token
            token_to_use = getattr(account, 'refresh_token', None) or getattr(account, 'access_token', None)
            if not token_to_use:
                logger.debug('No Google token available to revoke for %s', account)
                return False
            resp = requests.post(
                'https://oauth2.googleapis.com/revoke',
                params={'token': token_to_use},
                headers={'content-type': 'application/x-www-form-urlencoded'},
                timeout=10,
            )
            logger.info('Google revoke response %s for account %s (used refresh_token=%s)', resp.status_code, account, bool(getattr(account, 'refresh_token', None)))
            return resp.status_code == 200

    except Exception as exc:
        logger.exception('Failed to revoke token for %s: %s', account, exc)

    return False
