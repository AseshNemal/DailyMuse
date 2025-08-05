#!/usr/bin/env python3
"""
Multi-Platform Blog Bot
This version can post to multiple platforms: Dev.to, Hashnode, WordPress
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

class MultiPlatformBlogBot:
    def __init__(self):
        load_env()
        
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("Missing OpenAI API key")
        
        openai.api_key = self.openai_api_key
        
        # Platform configurations
        self.platforms = {
            "devto": {
                "api_key": os.getenv("DEVTO_API_KEY"),
                "url": "https://dev.to/api/articles",
                "enabled": bool(os.getenv("DEVTO_API_KEY"))
            },
            "hashnode": {
                "api_key": os.getenv("HASHNODE_API_KEY"),
                "publication_id": os.getenv("HASHNODE_PUBLICATION_ID"),
                "url": "https://api.hashnode.com",
                "enabled": bool(os.getenv("HASHNODE_API_KEY"))
            }
        }
        
        self.topics = [
            "The Future of AI in Software Development",
            "Building Scalable Web Applications in 2025",
            "The Rise of Edge Computing and IoT",
            "Cybersecurity Best Practices for Developers",
            "The Evolution of Cloud-Native Technologies",
            "Machine Learning for Beginners: A Practical Guide",
            "The Impact of 5G on Mobile Development",
            "Sustainable Software Engineering Practices",
            "The Future of Work in Tech Industry",
            "Blockchain Development: Beyond Cryptocurrency"
        ]
    
    def generate_content(self, topic: str) -> Dict[str, str]:
        """Generate blog content"""
        try:
            logger.info(f"Generating content for: {topic}")
            
            # Generate main content
            content_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a technical blog writer. Write engaging posts for developers.
                        
                        Guidelines:
                        - Use markdown formatting
                        - Include code examples where relevant
                        - Write 800-1000 words
                        - Use ## for headings
                        - Include practical tips and insights
                        - End with a call-to-action"""
                    },
                    {
                        "role": "user",
                        "content": f"Write a comprehensive blog post about: {topic}. Use markdown formatting."
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content = content_response["choices"][0]["message"]["content"]
            
            # Generate title
            title_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[
                    {
                        "role": "system",
                        "content": "Create engaging, SEO-friendly titles for tech blog posts."
                    },
                    {
                        "role": "user",
                        "content": f"Create a catchy title for: {topic}"
                    }
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            title = title_response["choices"][0]["message"]["content"].strip().strip('"')
            
            return {"title": title, "content": content}
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    def post_to_devto(self, title: str, content: str) -> Dict[str, Any]:
        """Post to Dev.to"""
        if not self.platforms["devto"]["enabled"]:
            return {"success": False, "error": "Dev.to not configured"}
        
        try:
            data = {
                "article": {
                    "title": title,
                    "body_markdown": content,
                    "published": True,
                    "tags": ["technology", "programming", "ai", "development"]
                }
            }
            
            headers = {
                "api-key": self.platforms["devto"]["api_key"],
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.platforms["devto"]["url"],
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                result = response.json()
                return {
                    "success": True,
                    "url": result.get("url"),
                    "platform": "Dev.to"
                }
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def post_to_hashnode(self, title: str, content: str) -> Dict[str, Any]:
        """Post to Hashnode"""
        if not self.platforms["hashnode"]["enabled"]:
            return {"success": False, "error": "Hashnode not configured"}
        
        try:
            query = """
            mutation CreatePublicationPost($input: CreatePostInput!) {
                createPublicationPost(input: $input) {
                    post {
                        id
                        title
                        url
                    }
                }
            }
            """
            
            variables = {
                "input": {
                    "title": title,
                    "contentMarkdown": content,
                    "publicationId": self.platforms["hashnode"]["publication_id"],
                    "tags": [
                        {"name": "technology"},
                        {"name": "programming"},
                        {"name": "ai"}
                    ]
                }
            }
            
            headers = {
                "Authorization": self.platforms["hashnode"]["api_key"],
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://api.hashnode.com",
                headers=headers,
                json={"query": query, "variables": variables}
            )
            
            if response.status_code == 200:
                result = response.json()
                if "data" in result and "createPublicationPost" in result["data"]:
                    post_data = result["data"]["createPublicationPost"]["post"]
                    return {
                        "success": True,
                        "url": post_data.get("url"),
                        "platform": "Hashnode"
                    }
            
            return {"success": False, "error": response.text}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run(self, platforms=None):
        """Main execution method"""
        if platforms is None:
            platforms = ["devto", "hashnode"]
        
        try:
            logger.info("🚀 Starting multi-platform blog posting...")
            
            # Generate content
            topic = random.choice(self.topics)
            logger.info(f"Selected topic: {topic}")
            
            blog_data = self.generate_content(topic)
            title = blog_data["title"]
            content = blog_data["content"]
            
            results = []
            
            # Post to selected platforms
            for platform in platforms:
                if platform == "devto":
                    result = self.post_to_devto(title, content)
                elif platform == "hashnode":
                    result = self.post_to_hashnode(title, content)
                else:
                    continue
                
                results.append(result)
                
                if result["success"]:
                    logger.info(f"✅ Posted to {result['platform']}: {result.get('url')}")
                else:
                    logger.error(f"❌ Failed to post to {platform}: {result.get('error')}")
            
            print(f"\n🎉 Blog Posting Results:")
            print(f"📝 Title: {title}")
            print(f"📄 Content: {len(content)} characters")
            
            for result in results:
                if result["success"]:
                    print(f"✅ {result['platform']}: {result.get('url')}")
                else:
                    print(f"❌ {result.get('platform', 'Unknown')}: Failed")
            
            return {
                "title": title,
                "content": content,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"❌ Multi-platform posting failed: {e}")
            raise

if __name__ == "__main__":
    bot = MultiPlatformBlogBot()
    bot.run()
