#!/usr/bin/env python3
"""
Simple OAuth setup for Blogger API with better error handling
"""

import os
import pickle
import webbrowser
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blogger API scope
SCOPES = ['https://www.googleapis.com/auth/blogger']

def setup_oauth_simple():
    """Simple OAuth setup with manual token entry"""
    
    print("🔧 Setting up Blogger OAuth Authentication")
    print("=" * 50)
    
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
        return False
    
    print("✅ Found credentials.json file")
    
    creds = None
    
    # Check for existing token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            print("✅ Found existing credentials")
    
    # If credentials are invalid, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            try:
                creds.refresh(Request())
                print("✅ Credentials refreshed successfully")
            except Exception as e:
                print(f"❌ Failed to refresh: {e}")
                creds = None
        
        if not creds:
            print("🚀 Starting OAuth flow...")
            try:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                
                # Try different methods
                try:
                    # Method 1: Local server
                    print("📱 Attempting to open browser for authentication...")
                    creds = flow.run_local_server(port=8080, open_browser=True)
                except Exception as e:
                    print(f"⚠️  Local server method failed: {e}")
                    try:
                        # Method 2: Console method
                        print("🔗 Using manual authentication method...")
                        creds = flow.run_console()
                    except Exception as e2:
                        print(f"❌ Both methods failed: {e2}")
                        return False
                
            except Exception as e:
                print(f"❌ OAuth flow failed: {e}")
                return False
        
        # Save credentials
        try:
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            print("✅ Credentials saved successfully")
        except Exception as e:
            print(f"⚠️  Warning: Could not save credentials: {e}")
    
    # Test the credentials
    try:
        print("🧪 Testing Blogger API connection...")
        service = build('blogger', 'v3', credentials=creds)
        
        # Get user's blogs
        blogs_result = service.blogs().listByUser(userId='self').execute()
        blogs = blogs_result.get('items', [])
        
        if blogs:
            print("\n🎉 SUCCESS! Authentication working!")
            print("📚 Your blogs:")
            for blog in blogs:
                print(f"   • {blog['name']}: {blog['url']}")
                print(f"     Blog ID: {blog['id']}")
                
                # Check if this is the target blog
                if 'dailymuset.blogspot.com' in blog['url']:
                    print(f"   🎯 This is your target blog!")
            
            return True
        else:
            print("⚠️  No blogs found for this account")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DailyMuse Blogger OAuth Setup")
    print("This will authenticate your Google account for Blogger API access\n")
    
    success = setup_oauth_simple()
    
    if success:
        print("\n" + "🎯 SETUP COMPLETE!")
        print("✅ OAuth authentication is working")
        print("✅ You can now post to your blog automatically")
        print("🚀 Ready to run the automated blogger bot!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        print("💡 Make sure you've configured the redirect URIs in Google Cloud Console")
