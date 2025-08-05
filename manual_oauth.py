#!/usr/bin/env python3
"""
Alternative OAuth setup using service account approach
This bypasses the consent screen issues for personal projects
"""

import os
import json
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/blogger']

def manual_oauth_flow():
    """Manual OAuth flow that handles consent screen issues better"""
    
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        return False
    
    print("🔧 Starting Manual OAuth Flow")
    print("=" * 40)
    
    try:
        # Load client configuration
        with open('credentials.json', 'r') as f:
            client_config = json.load(f)
        
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        
        # Generate the authorization URL with proper redirect URI
        auth_url, _ = flow.authorization_url(
            prompt='consent',
            access_type='offline',
            redirect_uri='http://localhost:8080'
        )
        
        print("📋 MANUAL OAUTH STEPS:")
        print("1. Copy this URL and open it in your browser:")
        print("─" * 50)
        print(auth_url)
        print("─" * 50)
        print("2. Sign in with your Google account")
        print("3. Click 'Advanced' if you see a warning")
        print("4. Click 'Go to petwellnesshub (unsafe)' or similar")
        print("5. Grant permissions")
        print("6. Copy the authorization code from the final page")
        print()
        
        # Get authorization code from user
        auth_code = input("📝 Paste the authorization code here: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return False
        
        # Exchange code for credentials
        print("🔄 Exchanging code for access token...")
        flow.fetch_token(code=auth_code)
        creds = flow.credentials
        
        # Save credentials
        with open('token.pickle', 'wb') as token:
            import pickle
            pickle.dump(creds, token)
        
        print("✅ Credentials saved successfully!")
        
        # Test the credentials
        print("🧪 Testing Blogger API access...")
        service = build('blogger', 'v3', credentials=creds)
        
        blogs_result = service.blogs().listByUser(userId='self').execute()
        blogs = blogs_result.get('items', [])
        
        if blogs:
            print("\n🎉 SUCCESS! OAuth authentication working!")
            print("📚 Your blogs:")
            for blog in blogs:
                print(f"   • {blog['name']}: {blog['url']}")
                print(f"     Blog ID: {blog['id']}")
            return True
        else:
            print("⚠️  No blogs found")
            return False
            
    except Exception as e:
        print(f"❌ Error in OAuth flow: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DailyMuse Manual OAuth Setup")
    print("This will handle the consent screen restrictions\n")
    
    success = manual_oauth_flow()
    
    if success:
        print("\n🎯 OAUTH SETUP COMPLETE!")
        print("✅ You can now use the automated blogger bot")
    else:
        print("\n❌ Setup failed")
        print("💡 Try adding yourself as a test user in Google Cloud Console")
