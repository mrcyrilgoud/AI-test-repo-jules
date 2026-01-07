from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.utils import parsedate_to_datetime

def get_gmail_service(credentials_dict):
    """
    Builds and returns the Gmail API service.
    """
    creds = Credentials(**credentials_dict)
    return build('gmail', 'v1', credentials=creds)

def fetch_recent_emails(service, max_results=10):
    """
    Fetches the most recent emails from the inbox.
    Returns a list of dictionaries containing simplified email data.
    """
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
    messages = results.get('messages', [])

    email_data = []

    if not messages:
        return []

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg.get('payload', {})
        headers = payload.get('headers', [])

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')

        # Get the body snippet
        snippet = msg.get('snippet', '')

        # Try to get full body content if needed (prioritizing plain text)
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode()
                        break
        elif 'body' in payload:
            data = payload['body'].get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode()

        if not body:
            body = snippet  # Fallback to snippet if body parsing fails

        email_data.append({
            'id': message['id'],
            'subject': subject,
            'sender': sender,
            'date': date_str,
            'snippet': snippet,
            'body': body
        })

    return email_data
