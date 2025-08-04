#!/usr/bin/env python3
"""
DailyMuse Blog Bot - Medium-ready Version
This version generates content and formats it for easy copy-paste to Medium
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

class MediumReadyBlogBot:
    def __init__(self):
        # Load environment variables from .env file if it exists
        load_env()
        
        # Load secrets from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            logger.error("Missing OPENAI_API_KEY in environment variables")
            print("⚠️ Please add your OpenAI API key to the .env file")
            print("💡 You can get credits at: https://platform.openai.com/account/billing")
            return
        
        # Setup OpenAI
        openai.api_key = self.openai_api_key
        
        # Blog topics pool
        self.topics = [
            "The future of artificial intelligence in everyday life",
            "How remote work is reshaping the modern workplace", 
            "The rise of sustainable technology and green innovation",
            "Digital transformation in healthcare: opportunities and challenges",
            "The evolution of cybersecurity in the digital age",
            "Smart cities and IoT: Building the urban future",
            "Blockchain beyond cryptocurrency: Real-world applications",
            "The psychology of user experience design",
            "Climate tech: Innovations fighting climate change",
            "The gig economy and future of freelance work",
            "Virtual reality applications beyond gaming",
            "Data privacy in the age of big data",
            "Machine learning democratization: AI for everyone",
            "The rise of no-code/low-code development",
            "Social media's impact on mental health and society",
            "Automation and the changing job market",
            "Digital wellness: Finding balance in a connected world",
            "The future of education: Online learning evolution",
            "Quantum computing: The next technological revolution", 
            "Sustainable software development practices"
        ]
    
    def generate_blog_content(self, topic: str) -> Dict[str, str]:
        """Generate blog content using OpenAI GPT-3.5"""
        try:
            logger.info(f"Generating blog content for topic: {topic}")
            
            # Generate the main content with Medium-optimized prompting
            content_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a professional Medium blog writer. Write engaging, informative, and well-structured blog posts optimized for Medium's audience. 

                        Guidelines:
                        - Use compelling storytelling and personal insights
                        - Include practical takeaways and actionable advice
                        - Write in a conversational yet professional tone
                        - Use subheadings to break up content
                        - Include relevant examples and case studies
                        - Make it 700-900 words for optimal Medium engagement
                        - End with a call-to-action or thought-provoking question"""
                    },
                    {
                        "role": "user", 
                        "content": f"Write a comprehensive Medium blog post about: {topic}. Make it engaging with personal insights, practical examples, and clear takeaways that readers can apply."
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            blog_content = content_response["choices"][0]["message"]["content"]
            
            # Generate a catchy, Medium-style title
            title_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a creative title writer specializing in Medium articles. Create compelling, click-worthy titles that perform well on Medium. 

                        Good Medium titles:
                        - Use numbers, questions, or bold statements
                        - Promise value or transformation
                        - Are specific and benefit-focused
                        - Create curiosity without being clickbait
                        - Are 60 characters or less for optimal display"""
                    },
                    {
                        "role": "user", 
                        "content": f"Create 3 engaging Medium article titles for this topic: {topic}. Choose the best one."
                    }
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            title = title_response["choices"][0]["message"]["content"].strip().strip('"')
            # Extract first title if multiple are provided
            if '\n' in title:
                title = title.split('\n')[0].strip('1234567890. ')
            
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
                print("💡 Usually $5-10 is enough for many blog posts")
            raise
    
    def generate_image_description(self, topic: str) -> str:
        """Generate a description for an image that can be created manually or with other tools"""
        descriptions = [
            f"A modern, minimalist illustration representing {topic} with clean lines and vibrant colors",
            f"An infographic-style image showing key concepts related to {topic}",
            f"A futuristic digital art piece visualizing {topic} in an engaging way",
            f"A professional header image with abstract elements representing {topic}",
            f"A creative visualization of {topic} using modern design principles"
        ]
        return random.choice(descriptions)
    
    def save_medium_ready_post(self, title: str, content: str, topic: str):
        """Save the blog in Medium-ready format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"medium_post_{timestamp}.md"
        
        # Generate tags for Medium
        tags = ["technology", "innovation", "future", "ai", "digital-transformation"]
        if "remote" in topic.lower():
            tags.extend(["remote-work", "workplace"])
        if "health" in topic.lower():
            tags.extend(["healthcare", "digital-health"])
        if "cyber" in topic.lower():
            tags.extend(["cybersecurity", "privacy"])
        if "sustain" in topic.lower():
            tags.extend(["sustainability", "green-tech"])
        
        # Format for Medium
        pub_date = datetime.now().strftime("%B %d, %Y")
        image_description = self.generate_image_description(topic)
        
        medium_content = f"""# {title}

*Published on {pub_date} | Generated by AI*

**Image suggestion:** {image_description}

{content}

---

*This blog post was automatically generated using AI technology. What are your thoughts on {topic.lower()}? Share your insights in the comments below!*

**Tags for Medium:** {', '.join(tags[:5])}
**Estimated reading time:** {len(content.split()) // 200 + 1} min read

---

**Instructions for posting to Medium:**
1. Copy the content above
2. Go to https://medium.com/new-story
3. Paste the title and content
4. Add the suggested tags
5. Add a header image (use the image suggestion above)
6. Preview and publish!
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(medium_content)
        
        logger.info(f"✅ Medium-ready post saved to: {filename}")
        return filename
    
    def run(self):
        """Main execution method"""
        try:
            if not hasattr(self, 'openai_api_key') or not self.openai_api_key:
                return None
                
            logger.info("🚀 Starting Medium-ready blog generation...")
            
            # Select a random topic
            topic = random.choice(self.topics)
            logger.info(f"Selected topic: {topic}")
            
            # Generate blog content
            blog_data = self.generate_blog_content(topic)
            title = blog_data["title"]
            content = blog_data["content"]
            
            # Save Medium-ready post
            filename = self.save_medium_ready_post(title, content, topic)
            
            logger.info("✅ Medium-ready blog generation completed!")
            
            print(f"\n🎉 Generated Medium-Ready Blog Post:")
            print(f"📝 Title: {title}")
            print(f"📄 Content: {len(content)} characters ({len(content.split())} words)")
            print(f"💾 Saved to: {filename}")
            print(f"\n📋 Next Steps:")
            print(f"1. Open the file: {filename}")
            print(f"2. Copy the content")
            print(f"3. Go to https://medium.com/new-story")
            print(f"4. Paste and publish!")
            
            return {
                "title": title,
                "content": content,
                "filename": filename,
                "topic": topic
            }
            
        except Exception as e:
            logger.error(f"❌ Blog generation failed: {str(e)}")
            return None

if __name__ == "__main__":
    bot = MediumReadyBlogBot()
    if bot:
        bot.run()
