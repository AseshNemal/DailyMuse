#!/usr/bin/env python3
"""
Simple OAuth setup using the standard flow
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

SCOPES = ['https://www.googleapis.com/auth/blogger']

def simple_oauth_setup():
    """Simple OAuth setup using standard flow"""
    
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        return False
    
    print("🔧 Setting up Blogger OAuth Authentication")
    print("=" * 50)
    
    creds = None
    
    # Check for existing token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        print("✅ Found existing credentials")
    
    # If there are no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            try:
                creds.refresh(Request())
                print("✅ Credentials refreshed")
            except Exception as e:
                print(f"⚠️  Refresh failed: {e}")
                creds = None
        
        if not creds:
            print("🚀 Starting OAuth flow...")
            print("📱 Your browser will open for authentication...")
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            
            try:
                # Try with port 8080
                creds = flow.run_local_server(port=8080, open_browser=True)
                print("✅ Authentication successful!")
            except Exception as e:
                print(f"⚠️  Port 8080 failed: {e}")
                try:
                    # Try with port 0 (auto-select)
                    creds = flow.run_local_server(port=0, open_browser=True)
                    print("✅ Authentication successful!")
                except Exception as e2:
                    print(f"❌ All ports failed: {e2}")
                    return False
        
        # Save the credentials
        try:
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            print("✅ Credentials saved to token.pickle")
        except Exception as e:
            print(f"⚠️  Could not save credentials: {e}")
    
    # Test the credentials
    try:
        print("🧪 Testing Blogger API connection...")
        service = build('blogger', 'v3', credentials=creds)
        
        # Get user's blogs
        blogs_result = service.blogs().listByUser(userId='self').execute()
        blogs = blogs_result.get('items', [])
        
        if blogs:
            print("\n🎉 SUCCESS! OAuth authentication working!")
            print("📚 Your blogs:")
            for blog in blogs:
                print(f"   • {blog['name']}: {blog['url']}")
                print(f"     Blog ID: {blog['id']}")
                
                # Update .env with correct Blog ID if this is the target blog
                if 'dailymuset.blogspot.com' in blog['url']:
                    print(f"   🎯 This is your target blog!")
                    print(f"   📝 Blog ID for .env: {blog['id']}")
            
            return True
        else:
            print("⚠️  No blogs found for this account")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Blogger API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DailyMuse Simple OAuth Setup")
    print("This will authenticate your Google account for Blogger API\n")
    
    success = simple_oauth_setup()
    
    if success:
        print("\n" + "🎯 OAUTH SETUP COMPLETE!")
        print("✅ Authentication working")
        print("✅ Credentials saved")
        print("🚀 Ready to run automated blogger bot!")
        print("\nNext step: Run the blogger bot to test posting!")
    else:
        print("\n❌ Setup failed")
        print("💡 Make sure you've added yourself as a test user")
