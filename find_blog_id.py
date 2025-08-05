#!/usr/bin/env python3
"""
Helper script to find your Blogger Blog ID
"""

import os
import requests
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def find_blog_id():
    """Find your Blog ID using the Blogger API"""
    load_env()
    
    api_key = os.getenv("BLOGGER_API_KEY")
    if not api_key:
        print("❌ BLOGGER_API_KEY not found in .env file")
        return
    
    print("🔍 Searching for your blogs...")
    
    # Get user's blogs
    url = "https://www.googleapis.com/blogger/v3/users/self/blogs"
    params = {"key": api_key}
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            if "items" in data and len(data["items"]) > 0:
                print(f"\n✅ Found {len(data['items'])} blog(s):")
                print("-" * 50)
                
                for i, blog in enumerate(data["items"], 1):
                    blog_id = blog.get("id")
                    name = blog.get("name")
                    url = blog.get("url")
                    
                    print(f"{i}. Blog Name: {name}")
                    print(f"   Blog ID: {blog_id}")
                    print(f"   URL: {url}")
                    print()
                
                print("💡 Copy the Blog ID (the long number) to your .env file")
                print("Example:")
                print(f"BLOGGER_BLOG_ID={data['items'][0].get('id')}")
            else:
                print("❌ No blogs found. Create a blog first at https://www.blogger.com/")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    find_blog_id()
