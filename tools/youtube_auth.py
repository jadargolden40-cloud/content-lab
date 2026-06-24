#!/usr/bin/env python3
"""
YouTube OAuth2 Authentication — run ONCE to generate youtube_token.json
Usage: python3 tools/youtube_auth.py
Needs: tools/youtube_credentials.json from Google Cloud Console
"""

import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
TOKEN = 'tools/youtube_token.json'
CREDS = 'tools/youtube_credentials.json'


def authenticate():
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS):
                print("\n❌ Missing tools/youtube_credentials.json")
                print("\nHow to get it:")
                print("  1. Go to https://console.cloud.google.com")
                print("  2. Create project → Enable YouTube Data API v3")
                print("  3. Credentials → Create OAuth 2.0 client ID → Download JSON")
                print(f"  4. Save as: {CREDS}")
                return
            flow = InstalledAppFlow.from_client_secrets_file(CREDS, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(TOKEN, 'w') as f:
            f.write(creds.to_json())
        print(f"✅ Token saved to {TOKEN}")

    print("✅ YouTube authenticated and ready!")


if __name__ == '__main__':
    authenticate()
