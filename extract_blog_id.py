#!/usr/bin/env python3
"""
Simple method to extract Blog ID from blog URL
"""

import requests
import re

def get_blog_id_from_url(blog_url):
    """Extract Blog ID from blog's HTML source"""
    try:
        print(f"🔍 Checking blog: {blog_url}")
        
        response = requests.get(blog_url)
        if response.status_code == 200:
            html_content = response.text
            
            # Search for blogId in the HTML
            blog_id_match = re.search(r'"blogId":"(\d+)"', html_content)
            if blog_id_match:
                blog_id = blog_id_match.group(1)
                print(f"✅ Found Blog ID: {blog_id}")
                return blog_id
            else:
                # Try alternative patterns
                alt_patterns = [
                    r'blogId=(\d+)',
                    r'"id":"(\d+)"',
                    r'data-blog-id="(\d+)"'
                ]
                
                for pattern in alt_patterns:
                    match = re.search(pattern, html_content)
                    if match:
                        blog_id = match.group(1)
                        print(f"✅ Found Blog ID (alt method): {blog_id}")
                        return blog_id
                
                print("❌ Could not find Blog ID in HTML")
                return None
        else:
            print(f"❌ Could not access blog: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    blog_url = "https://dailymuset.blogspot.com"
    blog_id = get_blog_id_from_url(blog_url)
    
    if blog_id:
        print("\n" + "="*50)
        print("🎉 SUCCESS! Add this to your .env file:")
        print(f"BLOGGER_BLOG_ID={blog_id}")
        print("="*50)
    else:
        print("\n❌ Could not find Blog ID automatically.")
        print("Please try the manual method:")
        print("1. Go to your blog")
        print("2. View page source")
        print("3. Search for 'blogId'")
