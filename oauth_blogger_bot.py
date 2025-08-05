#!/usr/bin/env python3
"""
OAuth-enabled Blogger Bot - Complete automated blogging system
"""

import os
import pickle
import logging
import random
from datetime import datetime
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OAuthBloggerBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        logger.info("Environment variables loaded from .env file")
        
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.blog_id = os.getenv('BLOGGER_BLOG_ID')
        
        if not self.openai_api_key or not self.blog_id:
            raise ValueError("Missing OPENAI_API_KEY or BLOGGER_BLOG_ID in .env file")
        
        # Set up OpenAI
        openai.api_key = self.openai_api_key
        
        # Load OAuth credentials
        self.credentials = self.load_credentials()
        if not self.credentials:
            raise ValueError("OAuth credentials not found. Run simple_oauth.py first!")
        
        # Set up Blogger service
        self.service = build('blogger', 'v3', credentials=self.credentials)
        
        logger.info("✅ OAuth Blogger Bot initialized successfully")

    def load_credentials(self):
        """Load OAuth credentials from token.pickle"""
        if not os.path.exists('token.pickle'):
            logger.error("❌ token.pickle not found. Run OAuth setup first!")
            return None
        
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
            
            # Refresh if needed
            if creds.expired and creds.refresh_token:
                logger.info("🔄 Refreshing expired credentials...")
                creds.refresh(Request())
                
                # Save refreshed credentials
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            
            logger.info("✅ OAuth credentials loaded successfully")
            return creds
            
        except Exception as e:
            logger.error(f"❌ Error loading credentials: {e}")
            return None

    def generate_sample_content(self):
        """Generate sample content for testing (fallback when OpenAI quota exceeded)"""
        topics = [
            "The Future of Remote Work in 2025",
            "Building Sustainable Habits for Success",
            "The Art of Digital Minimalism",
            "Embracing Change in Uncertain Times",
            "The Power of Consistent Daily Actions"
        ]
        
        topic = random.choice(topics)
        current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        content = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>🌟 {topic}</h2>
            
            <p>Welcome to another insightful post from DailyMuse! Today, we're exploring an important topic that affects many of us in our daily lives.</p>
            
            <h3>📖 Introduction</h3>
            <p>In today's fast-paced world, it's essential to take a step back and reflect on the changes happening around us. This post will dive deep into {topic.lower()} and provide practical insights you can apply immediately.</p>
            
            <h3>🔍 Key Insights</h3>
            <ul>
                <li><strong>Mindful Approach:</strong> Taking time to understand the core principles</li>
                <li><strong>Practical Application:</strong> Real-world strategies that work</li>
                <li><strong>Long-term Vision:</strong> Building sustainable practices for the future</li>
                <li><strong>Community Impact:</strong> How these changes affect others around us</li>
            </ul>
            
            <blockquote style="border-left: 4px solid #007acc; padding-left: 20px; margin: 20px 0; font-style: italic; color: #555;">
                "Success is not final, failure is not fatal: it is the courage to continue that counts." - Winston Churchill
            </blockquote>
            
            <h3>🚀 Taking Action</h3>
            <p>The most important part of any learning is implementation. Here are some practical steps you can take today:</p>
            
            <ol>
                <li>Start with small, manageable changes</li>
                <li>Track your progress consistently</li>
                <li>Seek feedback from trusted mentors or peers</li>
                <li>Adjust your approach based on results</li>
                <li>Celebrate small wins along the way</li>
            </ol>
            
            <h3>💭 Final Thoughts</h3>
            <p>Remember, every expert was once a beginner. The journey of growth and improvement is ongoing, and each step forward is valuable progress.</p>
            
            <p>What are your thoughts on {topic.lower()}? Share your experiences in the comments below!</p>
            
            <hr style="margin: 30px 0; border: none; border-top: 2px solid #eee;">
            <p style="text-align: center; color: #888; font-size: 14px;">
                <em>📝 This post was created by DailyMuse on {current_time} | Follow us for daily inspiration! 🚀</em>
            </p>
        </div>
        """
        
        return {
            'title': f"🌟 {topic} - Daily Inspiration",
            'content': content,
            'topic': topic
        }

    def generate_ai_content(self, topic):
        """Generate blog content using OpenAI (when quota available)"""
        try:
            # Generate blog content
            content_prompt = f"""
            Write a comprehensive, engaging blog post about "{topic}" for a daily inspiration blog called DailyMuse.
            
            Requirements:
            - 600-800 words
            - Professional but friendly tone
            - Include practical advice and actionable insights
            - Use HTML formatting with proper headings, paragraphs, and lists
            - Include a compelling introduction and strong conclusion
            - Add relevant quotes or statistics if appropriate
            
            The post should inspire and educate readers while being easy to read and implement.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional blog writer who creates inspiring, practical content for a daily motivation blog."},
                    {"role": "user", "content": content_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            return {
                'title': f"🌟 {topic} - Daily Inspiration",
                'content': content,
                'topic': topic
            }
            
        except Exception as e:
            logger.warning(f"⚠️  OpenAI API error: {e}")
            logger.info("🔄 Falling back to sample content...")
            return self.generate_sample_content()

    def post_to_blogger(self, title, content):
        """Post content to Blogger using OAuth"""
        try:
            logger.info("🚀 Posting to Blogger...")
            logger.info(f"📝 Title: {title}")
            
            post_data = {
                'kind': 'blogger#post',
                'title': title,
                'content': content
            }
            
            # Post to Blogger
            result = self.service.posts().insert(blogId=self.blog_id, body=post_data).execute()
            
            post_url = result.get('url', 'Unknown URL')
            post_id = result.get('id', 'Unknown ID')
            
            logger.info(f"✅ Successfully posted to Blogger!")
            logger.info(f"🔗 Post URL: {post_url}")
            logger.info(f"📋 Post ID: {post_id}")
            
            return True, post_url
            
        except Exception as e:
            logger.error(f"❌ Error posting to Blogger: {e}")
            return False, None

    def run(self):
        """Run the complete blogging workflow"""
        try:
            logger.info("🚀 Starting automated Blogger posting...")
            
            # Generate content
            blog_data = self.generate_sample_content()  # Using sample for now
            logger.info(f"✅ Generated content: {blog_data['topic']}")
            
            # Post to Blogger
            success, post_url = self.post_to_blogger(blog_data['title'], blog_data['content'])
            
            if success:
                logger.info("🎉 Automated blog posting completed successfully!")
                logger.info(f"🌐 Check your post at: {post_url}")
                return True
            else:
                logger.error("❌ Blog posting failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Automated blog posting failed: {e}")
            return False

if __name__ == "__main__":
    try:
        bot = OAuthBloggerBot()
        success = bot.run()
        
        if success:
            print("\n🎯 SUCCESS! Your blog post has been published!")
            print("🌐 Visit: https://dailymuset.blogspot.com")
        else:
            print("\n❌ Failed to publish blog post")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you've run the OAuth setup first!")
