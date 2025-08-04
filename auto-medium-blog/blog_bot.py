import os
import openai
import requests
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
    env_path = Path(__file__).parent.parent / '.env'
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        logger.info("Environment variables loaded from .env file")

class MediumBlogBot:
    def __init__(self):
        # Load environment variables from .env file if it exists
        load_env()
        
        # Load secrets from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.medium_token = os.getenv("MEDIUM_TOKEN")
        
        if not self.openai_api_key or not self.medium_token:
            logger.error("Missing required environment variables: OPENAI_API_KEY or MEDIUM_TOKEN")
            logger.error("Please set them in .env file or as environment variables")
            raise ValueError("Missing required API keys")
        
        # Setup OpenAI
        openai.api_key = self.openai_api_key
        
        # Blog topics pool
        self.topics = [
            "The future of artificial intelligence in everyday life",
            "How remote work is reshaping the modern workplace",
            "The rise of sustainable technology and green innovation",
            "Digital transformation in healthcare: opportunities and challenges",
            "The evolution of cybersecurity in the digital age",
            "Blockchain technology beyond cryptocurrency",
            "The impact of social media on mental health and society",
            "Climate change solutions through technology",
            "The future of education with AI and virtual reality",
            "Data privacy in the age of big data",
            "The gig economy and the future of work",
            "Smart cities and urban technology integration",
            "The psychology of user experience design",
            "Automation and the changing job market",
            "The role of technology in combating social inequality",
            "Virtual reality and its applications beyond gaming",
            "The importance of digital literacy in modern society",
            "Sustainable living with smart home technology",
            "The ethics of artificial intelligence development",
            "How machine learning is revolutionizing industries"
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
    
    def should_use_image(self) -> bool:
        """Determine if we should use an image (every other day to optimize costs)"""
        # Use day of year to determine if we should generate image
        day_of_year = datetime.now().timetuple().tm_yday
        return day_of_year % 2 == 0
    
    def format_html_content(self, title: str, content: str, image_url: Optional[str] = None) -> str:
        """Format the blog content as HTML"""
        
        # Add image if provided
        image_html = ""
        if image_url:
            image_html = f'<div style="text-align: center; margin: 20px 0;"><img src="{image_url}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 8px;"/></div>'
        
        # Format content with proper HTML
        formatted_content = content.replace('\n\n', '</p><p>').replace('\n', '<br/>')
        
        # Add publication info
        pub_date = datetime.now().strftime("%B %d, %Y")
        
        html_content = f"""<h1>{title}</h1>
{image_html}
<p><em>Published on {pub_date} | Generated by AI</em></p>
<p>{formatted_content}</p>
<hr/>
<p><em>This blog post was automatically generated using AI technology. Stay tuned for more insights on technology, innovation, and the future!</em></p>"""
        
        return html_content
    
    def get_medium_user_id(self) -> str:
        """Get the Medium user ID"""
        try:
            headers = {
                "Authorization": f"Bearer {self.medium_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            
            response = requests.get("https://api.medium.com/v1/me", headers=headers)
            response.raise_for_status()
            
            user_id = response.json()["data"]["id"]
            logger.info(f"Retrieved Medium user ID: {user_id}")
            return user_id
            
        except Exception as e:
            logger.error(f"Error getting Medium user ID: {str(e)}")
            raise
    
    def post_to_medium(self, title: str, html_content: str) -> Dict[str, Any]:
        """Post the blog to Medium"""
        try:
            logger.info(f"Posting blog to Medium: {title}")
            
            user_id = self.get_medium_user_id()
            
            headers = {
                "Authorization": f"Bearer {self.medium_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            
            post_data = {
                "title": title,
                "contentFormat": "html",
                "content": html_content,
                "publishStatus": "public",
                "tags": ["technology", "ai", "innovation", "future", "automation"]
            }
            
            response = requests.post(
                f"https://api.medium.com/v1/users/{user_id}/posts",
                headers=headers, 
                json=post_data
            )
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"✅ Blog posted successfully: {result['data']['url']}")
                return result["data"]
            else:
                logger.error(f"❌ Failed to post blog: {response.status_code} - {response.text}")
                raise Exception(f"Failed to post: {response.text}")
                
        except Exception as e:
            logger.error(f"Error posting to Medium: {str(e)}")
            raise
    
    def run(self):
        """Main execution method"""
        try:
            logger.info("🚀 Starting automated blog posting process...")
            
            # Select a random topic
            topic = random.choice(self.topics)
            logger.info(f"Selected topic: {topic}")
            
            # Generate blog content
            blog_data = self.generate_blog_content(topic)
            title = blog_data["title"]
            content = blog_data["content"]
            
            # Generate image if it's an image day
            image_url = None
            if self.should_use_image():
                logger.info("📸 Today is an image day - generating AI image...")
                image_url = self.generate_image(topic)
            else:
                logger.info("📝 Today is a text-only day - skipping image generation...")
            
            # Format HTML content
            html_content = self.format_html_content(title, content, image_url)
            
            # Post to Medium
            post_result = self.post_to_medium(title, html_content)
            
            logger.info("✅ Blog posting process completed successfully!")
            return post_result
            
        except Exception as e:
            logger.error(f"❌ Blog posting process failed: {str(e)}")
            raise

if __name__ == "__main__":
    bot = MediumBlogBot()
    bot.run()
