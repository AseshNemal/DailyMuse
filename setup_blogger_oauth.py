#!/usr/bin/env python3
"""
Setup OAuth2 authentication for Blogger API
This will create the necessary credentials for posting to Blogger
"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blogger API scope for reading and writing
SCOPES = ['https://www.googleapis.com/auth/blogger']

def setup_blogger_oauth():
    """Set up OAuth2 authentication for Blogger API"""
    
    print("🔧 Setting up Blogger OAuth Authentication")
    print("=" * 50)
    
    print("\n📋 To complete this setup, you need to:")
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable the Blogger API v3")
    print("4. Create OAuth 2.0 credentials (Desktop application)")
    print("5. Download the credentials JSON file")
    print("6. Rename it to 'credentials.json' and put it in this folder")
    
    print("\n🔍 Detailed Steps:")
    print("─" * 30)
    print("1. Visit: https://console.cloud.google.com/apis/library/blogger-v3.googleapis.com")
    print("2. Click 'Enable' on Blogger API v3")
    print("3. Go to: https://console.cloud.google.com/apis/credentials")
    print("4. Click '+ CREATE CREDENTIALS' → 'OAuth client ID'")
    print("5. Choose 'Desktop application'")
    print("6. Name it 'DailyMuse Blogger Bot'")
    print("7. Download the JSON file")
    print("8. Rename to 'credentials.json' and place in this directory")
    
    print("\n" + "=" * 50)
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        print("Please follow the steps above and run this script again.")
        return False
    
    print("✅ Found credentials.json file")
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🚀 Starting OAuth flow...")
            print("📱 Your browser will open for authentication")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
        print("✅ Credentials saved to token.pickle")
    
    # Test the credentials
    try:
        service = build('blogger', 'v3', credentials=creds)
        
        # Try to get blog info
        blogs_result = service.blogs().listByUser(userId='self').execute()
        blogs = blogs_result.get('items', [])
        
        if blogs:
            print("\n🎉 SUCCESS! OAuth authentication working!")
            print("📚 Your blogs:")
            for blog in blogs:
                print(f"   • {blog['name']}: {blog['url']}")
                print(f"     Blog ID: {blog['id']}")
            
            print("\n✅ You can now use the OAuth-enabled blogger bot!")
            return True
        else:
            print("⚠️  Authentication successful but no blogs found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing credentials: {e}")
        return False

if __name__ == "__main__":
    success = setup_blogger_oauth()
    
    if success:
        print("\n" + "🎯 NEXT STEPS:")
        print("1. The OAuth setup is complete!")
        print("2. You can now run the OAuth-enabled blogger bot")
        print("3. Your credentials are saved in token.pickle")
    else:
        print("\n❌ Setup incomplete. Please follow the instructions above.")
