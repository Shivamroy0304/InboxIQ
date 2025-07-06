import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from notifier import send_summary, make_voice_call
import base64
import re
from setuptools import setup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")


IMPORTANT_SENDERS = {
    "noreply.cdcinfo@vitstudent.ac.in",
    "vitianscdc2026@vitstudent.ac.in"
}
KEYWORD = "dr. v. samuel rajkumar"

def gmail_authenticate():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def get_unread_emails(service):
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=10).execute()
    messages = results.get('messages', [])

    print(f"🔔 You have {len(messages)} unread email(s).")

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()

        headers = msg_data['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "")
        snippet = msg_data.get("snippet", "")

        
        match = re.search(r"<(.+?)>", sender)
        email_cleaned = match.group(1) if match else sender.lower()

    
        try:
            parts = msg_data['payload'].get('parts', [])
            body = ""
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    decoded = base64.urlsafe_b64decode(data).decode("utf-8")
                    body += decoded
        except Exception:
            body = snippet

        
        if email_cleaned in IMPORTANT_SENDERS and KEYWORD.lower() in body.lower():
            print("✅ Important email matched, triggering call and Telegram...")
            message = f"📧 From: {email_cleaned}\nSubject: {subject}\n\n{snippet}"
            send_summary(message)
            make_voice_call(message)
        else:
            print("📭 Not from important sender or keyword missing, skipping.")

if __name__ == "__main__":
    service = gmail_authenticate()
    get_unread_emails(service)
    
