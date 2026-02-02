from google_auth_oauthlib.flow import Flow

def make_google_flow(client_secrets_file, scopes, redirect_uri):
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=scopes,
        redirect_uri=redirect_uri,
    )
    return flow
