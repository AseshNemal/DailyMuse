#!/usr/bin/env python3
"""
Test version of DailyMuse Blog Bot
This version generates content without posting to Medium (for testing)
"""

import os
import openai
import random
import json
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

class TestBlogBot:
    def __init__(self):
        # Load environment variables from .env file if it exists
        load_env()
        
        # Load secrets from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            logger.error("Missing OPENAI_API_KEY in environment variables")
            raise ValueError("Missing OpenAI API key")
        
        # Setup OpenAI
        openai.api_key = self.openai_api_key
        
        # Blog topics pool
        self.topics = [
            "The future of artificial intelligence in everyday life",
            "How remote work is reshaping the modern workplace",
            "The rise of sustainable technology and green innovation",
            "Digital transformation in healthcare: opportunities and challenges",
            "The evolution of cybersecurity in the digital age"
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
                        Include an introduction, main body with clear points, and a conclusion. 
                        Write in a conversational yet professional tone. 
                        Make the content approximately 600-800 words."""
                    },
                    {
                        "role": "user", 
                        "content": f"Write a comprehensive blog post about: {topic}. Include practical insights and real-world examples."
                    }
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            blog_content = content_response["choices"][0]["message"]["content"]
            
            # Generate a catchy title
            title_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a creative title writer. Create catchy, engaging blog titles that would attract readers."
                    },
                    {
                        "role": "user", 
                        "content": f"Create an engaging blog post title for this topic: {topic}"
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
            raise
    
    def generate_image(self, topic: str) -> Optional[str]:
        """Generate an image using DALL-E"""
        try:
            logger.info(f"Generating image for topic: {topic}")
            
            # Create a more detailed image prompt
            image_prompt = f"A modern, professional illustration representing {topic}. Clean, minimalist design with vibrant colors, suitable for a blog post header."
            
            image_response = openai.Image.create(
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            
            image_url = image_response["data"][0]["url"]
            logger.info(f"Image generated successfully: {image_url}")
            return image_url
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return None
    
    def save_blog_to_file(self, title: str, content: str, image_url: Optional[str] = None):
        """Save the blog to a local file for testing"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_post_{timestamp}.html"
        
        # Add image if provided
        image_html = ""
        if image_url:
            image_html = f'<div style="text-align: center; margin: 20px 0;"><img src="{image_url}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 8px;"/></div>'
        
        # Format content with proper HTML
        formatted_content = content.replace('\n\n', '</p><p>').replace('\n', '<br/>')
        
        # Add publication info
        pub_date = datetime.now().strftime("%B %d, %Y")
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        img {{ max-width: 100%; height: auto; }}
        .meta {{ color: #666; font-style: italic; }}
        hr {{ border: 1px solid #eee; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    {image_html}
    <p class="meta">Published on {pub_date} | Generated by AI</p>
    <p>{formatted_content}</p>
    <hr/>
    <p class="meta">This blog post was automatically generated using AI technology. Stay tuned for more insights on technology, innovation, and the future!</p>
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Blog saved to file: {filename}")
        return filename
    
    def run(self):
        """Main execution method"""
        try:
            logger.info("🚀 Starting blog generation process...")
            
            # Select a random topic
            topic = random.choice(self.topics)
            logger.info(f"Selected topic: {topic}")
            
            # Generate blog content
            blog_data = self.generate_blog_content(topic)
            title = blog_data["title"]
            content = blog_data["content"]
            
            # Generate image (optional)
            logger.info("📸 Generating AI image...")
            image_url = self.generate_image(topic)
            
            # Save to file instead of posting
            filename = self.save_blog_to_file(title, content, image_url)
            
            logger.info("✅ Blog generation completed successfully!")
            
            print(f"\n🎉 Generated Blog Post:")
            print(f"📝 Title: {title}")
            print(f"📄 Content: {len(content)} characters")
            print(f"🖼️  Image: {'Yes' if image_url else 'No'}")
            print(f"💾 Saved to: {filename}")
            
            return {
                "title": title,
                "content": content,
                "image_url": image_url,
                "filename": filename
            }
            
        except Exception as e:
            logger.error(f"❌ Blog generation failed: {str(e)}")
            raise

if __name__ == "__main__":
    bot = TestBlogBot()
    bot.run()
