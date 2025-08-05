#!/usr/bin/env python3
"""
Automated Blogger Bot
This version automatically posts to Blogger using Google's official API
"""

import os
import openai
import random
import json
import requests
from datetime import datetime
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.info("Environment variables loaded from .env file")

class BloggerBot:
    def __init__(self):
        # Load environment variables
        load_env()
        
        # Load secrets from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.blogger_api_key = os.getenv("BLOGGER_API_KEY")
        self.blog_id = os.getenv("BLOGGER_BLOG_ID")
        
        if not self.openai_api_key:
            logger.error("Missing OPENAI_API_KEY in environment variables")
            raise ValueError("Missing OpenAI API key")
            
        if not self.blogger_api_key:
            logger.error("Missing BLOGGER_API_KEY in environment variables")
            logger.info("Get your API key from: https://console.developers.google.com/")
            raise ValueError("Missing Blogger API key")
            
        if not self.blog_id:
            logger.error("Missing BLOGGER_BLOG_ID in environment variables")
            logger.info("Find your Blog ID in Blogger settings")
            raise ValueError("Missing Blog ID")
        
        # Setup OpenAI
        openai.api_key = self.openai_api_key
        
        # Blog topics pool
        self.topics = [
            "The Future of Artificial Intelligence in Everyday Life",
            "How Remote Work is Reshaping the Modern Workplace",
            "The Rise of Sustainable Technology and Green Innovation",
            "Digital Transformation in Healthcare: Opportunities and Challenges",
            "The Evolution of Cybersecurity in the Digital Age",
            "Smart Cities: Building the Urban Future with IoT",
            "Blockchain Beyond Cryptocurrency: Real-World Applications",
            "The Psychology of User Experience Design",
            "Climate Tech: Innovations Fighting Climate Change",
            "The Gig Economy and Future of Freelance Work",
            "Virtual Reality Applications Beyond Gaming",
            "Data Privacy in the Age of Big Data",
            "Machine Learning Democratization: AI for Everyone",
            "The Rise of No-Code/Low-Code Development Platforms",
            "Social Media's Impact on Mental Health and Society",
            "Automation and the Changing Job Market Landscape",
            "Digital Wellness: Finding Balance in a Connected World",
            "The Future of Education: Online Learning Evolution",
            "Quantum Computing: The Next Technological Revolution",
            "Sustainable Software Development Practices"
        ]
    
    def generate_blog_content(self, topic: str) -> Dict[str, str]:
        """Generate blog content using OpenAI GPT-3.5"""
        try:
            logger.info(f"Generating blog content for topic: {topic}")
            
            # Generate the main content
            content_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a professional blog writer. Write engaging, informative, and well-structured blog posts. 

                        Guidelines:
                        - Use compelling storytelling and personal insights
                        - Include practical takeaways and actionable advice
                        - Write in a conversational yet professional tone
                        - Use HTML headings (<h2>, <h3>) to break up content
                        - Include relevant examples and case studies
                        - Make it 800-1000 words for optimal engagement
                        - End with a call-to-action or thought-provoking question
                        - Use HTML formatting for better presentation"""
                    },
                    {
                        "role": "user", 
                        "content": f"Write a comprehensive blog post about: {topic}. Make it engaging with personal insights, practical examples, and clear takeaways. Use HTML formatting with <h2> and <h3> headings, <p> paragraphs, and <strong> for emphasis."
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            blog_content = content_response["choices"][0]["message"]["content"]
            
            # Generate a catchy title
            title_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a creative title writer. Create compelling, SEO-friendly titles. 

                        Good blog titles:
                        - Use numbers, questions, or bold statements
                        - Promise value or transformation
                        - Are specific and benefit-focused
                        - Create curiosity without being clickbait
                        - Are 60 characters or less for SEO"""
                    },
                    {
                        "role": "user", 
                        "content": f"Create one engaging blog title for this topic: {topic}. Just return the title, nothing else."
                    }
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            title = title_response["choices"][0]["message"]["content"].strip().strip('"')
            
            return {
                "title": title,
                "content": blog_content
            }
            
        except Exception as e:
            logger.error(f"Error generating blog content: {str(e)}")
            if "insufficient_quota" in str(e):
                print("\n💳 OpenAI API Quota Exceeded!")
                print("Please add billing to your OpenAI account:")
                print("🔗 https://platform.openai.com/account/billing")
            raise
    
    def generate_image_description(self, topic: str) -> str:
        """Generate a description for an image"""
        descriptions = [
            f"A modern, vibrant illustration representing {topic}",
            f"An infographic showing key concepts of {topic}",
            f"A futuristic digital art piece about {topic}",
            f"A professional header image for {topic}",
            f"A creative visualization of {topic} concepts"
        ]
        return random.choice(descriptions)
    
    def format_blog_content(self, title: str, content: str, topic: str) -> str:
        """Format the blog content with additional elements"""
        
        pub_date = datetime.now().strftime("%B %d, %Y")
        image_desc = self.generate_image_description(topic)
        
        # Add introduction and footer
        formatted_content = f"""
<div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
<p><strong>📅 Published:</strong> {pub_date} | <strong>🤖 Generated by:</strong> AI Technology</p>
<p><strong>🖼️ Featured Image Suggestion:</strong> {image_desc}</p>
</div>

{content}

<hr style="margin: 30px 0;">

<div style="background: #e9ecef; padding: 20px; border-radius: 8px;">
<h3>💭 What's Your Take?</h3>
<p>This blog post was automatically generated using AI technology. What are your thoughts on <strong>{topic.lower()}</strong>? Share your insights in the comments below!</p>

<p><strong>🏷️ Tags:</strong> Technology, Innovation, AI, Future, Digital Transformation</p>
</div>

<div style="margin-top: 20px; text-align: center; font-size: 0.9em; color: #666;">
<p>🚀 <strong>Daily AI Insights</strong> - Exploring technology, innovation, and the future</p>
</div>
"""
        
        return formatted_content
    
    def post_to_blogger(self, title: str, content: str, topic: str) -> Dict[str, Any]:
        """Post the blog to Blogger using API"""
        try:
            logger.info(f"Posting blog to Blogger: {title}")
            
            # Format content
            formatted_content = self.format_blog_content(title, content, topic)
            
            # Prepare the post data
            post_data = {
                "kind": "blogger#post",
                "title": title,
                "content": formatted_content,
                "labels": ["technology", "ai", "innovation", "future", "automation"]
            }
            
            # Blogger API endpoint
            url = f"https://www.googleapis.com/blogger/v3/blogs/{self.blog_id}/posts"
            
            # Headers
            headers = {
                "Content-Type": "application/json",
            }
            
            # Parameters
            params = {
                "key": self.blogger_api_key
            }
            
            # Make the API request
            response = requests.post(
                url,
                headers=headers,
                params=params,
                data=json.dumps(post_data)
            )
            
            if response.status_code == 200:
                result = response.json()
                blog_url = result.get("url", "Unknown")
                logger.info(f"✅ Blog posted successfully to Blogger!")
                logger.info(f"🔗 URL: {blog_url}")
                
                return {
                    "success": True,
                    "url": blog_url,
                    "id": result.get("id"),
                    "published": result.get("published")
                }
            else:
                logger.error(f"❌ Failed to post blog: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error posting to Blogger: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def run(self):
        """Main execution method"""
        try:
            logger.info("🚀 Starting automated Blogger posting...")
            
            # Select a random topic
            topic = random.choice(self.topics)
            logger.info(f"Selected topic: {topic}")
            
            # Generate blog content
            blog_data = self.generate_blog_content(topic)
            title = blog_data["title"]
            content = blog_data["content"]
            
            logger.info(f"Generated content: {len(content)} characters")
            
            # Post to Blogger
            result = self.post_to_blogger(title, content, topic)
            
            if result.get("success"):
                logger.info("✅ Automated blog posting completed successfully!")
                print(f"\n🎉 Successfully Posted to Blogger:")
                print(f"📝 Title: {title}")
                print(f"📄 Content: {len(content)} characters")
                print(f"🌐 URL: {result.get('url', 'Check your Blogger dashboard')}")
                
                return {
                    "title": title,
                    "content": content,
                    "url": result.get("url"),
                    "success": True
                }
            else:
                raise Exception(f"Failed to post to Blogger: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"❌ Automated blog posting failed: {str(e)}")
            raise

if __name__ == "__main__":
    bot = BloggerBot()
    bot.run()
