#!/usr/bin/env python3
"""
Test Blogger posting with sample content (no OpenAI API needed)
"""

import os
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BloggerTester:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        logger.info("Environment variables loaded from .env file")
        
        self.api_key = os.getenv('BLOGGER_API_KEY')
        self.blog_id = os.getenv('BLOGGER_BLOG_ID')
        
        if not self.api_key or not self.blog_id:
            raise ValueError("Missing BLOGGER_API_KEY or BLOGGER_BLOG_ID in .env file")
        
        logger.info(f"✅ Blogger API Key: {self.api_key[:20]}...")
        logger.info(f"✅ Blog ID: {self.blog_id}")

    def create_sample_post(self):
        """Create a sample blog post to test the API"""
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        title = f"🤖 Test Post - {current_time}"
        
        content = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Welcome to DailyMuse!</h2>
            
            <p>This is a <strong>test post</strong> created by our automated blogging system on {current_time}.</p>
            
            <h3>✨ What This System Can Do:</h3>
            <ul>
                <li>🎯 Generate AI-powered blog content</li>
                <li>🖼️ Create beautiful images with DALL-E</li>  
                <li>📝 Format posts with proper HTML</li>
                <li>🚀 Post automatically to Blogger</li>
                <li>⏰ Run daily via GitHub Actions</li>
            </ul>
            
            <h3>🔧 Technical Features:</h3>
            <p>Our system uses:</p>
            <ul>
                <li><strong>OpenAI GPT-3.5</strong> for content generation</li>
                <li><strong>DALL-E</strong> for image creation</li>
                <li><strong>Blogger API v3</strong> for reliable posting</li>
                <li><strong>GitHub Actions</strong> for automation</li>
            </ul>
            
            <blockquote style="border-left: 4px solid #007acc; padding-left: 20px; margin: 20px 0; font-style: italic; color: #555;">
                "The future of content creation is here - automated, intelligent, and always on schedule!"
            </blockquote>
            
            <p>🎉 If you're seeing this post, it means the Blogger API integration is working perfectly!</p>
            
            <hr style="margin: 30px 0; border: none; border-top: 2px solid #eee;">
            <p style="text-align: center; color: #888; font-size: 14px;">
                <em>This post was automatically generated and published by DailyMuse 🚀</em>
            </p>
        </div>
        """
        
        return {
            'title': title,
            'content': content
        }

    def post_to_blogger(self, title, content):
        """Post content to Blogger using the API"""
        url = f'https://www.googleapis.com/blogger/v3/blogs/{self.blog_id}/posts'
        
        post_data = {
            'kind': 'blogger#post',
            'title': title,
            'content': content
        }
        
        params = {
            'key': self.api_key
        }
        
        logger.info("🚀 Posting to Blogger...")
        logger.info(f"📝 Title: {title}")
        
        try:
            response = requests.post(url, json=post_data, params=params)
            logger.info(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                post_info = response.json()
                post_url = post_info.get('url', 'Unknown URL')
                logger.info(f"✅ Successfully posted to Blogger!")
                logger.info(f"🔗 Post URL: {post_url}")
                return True
            else:
                logger.error(f"❌ Failed to post: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error posting to Blogger: {e}")
            return False

    def run_test(self):
        """Run the complete test"""
        try:
            logger.info("🧪 Starting Blogger API test...")
            
            # Create sample post
            blog_data = self.create_sample_post()
            logger.info("✅ Sample blog content created")
            
            # Post to Blogger
            success = self.post_to_blogger(blog_data['title'], blog_data['content'])
            
            if success:
                logger.info("🎉 TEST PASSED! Blogger integration is working perfectly!")
                logger.info("🌐 Check your blog at: https://dailymuset.blogspot.com")
            else:
                logger.error("❌ TEST FAILED! Check the error messages above.")
                
        except Exception as e:
            logger.error(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    tester = BloggerTester()
    tester.run_test()
