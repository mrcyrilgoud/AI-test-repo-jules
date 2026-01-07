import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

# Scopes required for the application
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_flow(redirect_uri):
    """
    Creates and returns a Google OAuth2 Flow instance.
    """
    client_config = {
        "web": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    return Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

def credentials_to_dict(credentials):
    """
    Converts Google Credentials object to a dictionary for session storage.
    """
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
