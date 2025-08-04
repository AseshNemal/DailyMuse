#!/usr/bin/env python3
"""
Automated Medium Blog Bot
This version automatically posts to Medium using web automation
"""

import os
import openai
import random
import json
import time
from datetime import datetime
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
    else:
        logger.warning(f".env file not found at {env_path}")
        # Try parent directory
        env_path_parent = Path(__file__).parent.parent / '.env'
        if env_path_parent.exists():
            with open(env_path_parent, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
            logger.info("Environment variables loaded from parent .env file")
        else:
            logger.error(f"No .env file found at {env_path} or {env_path_parent}")

class AutoMediumBlogBot:
    def __init__(self):
        # Load environment variables
        load_env()
        
        # Load secrets from environment
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_email = os.getenv("GOOGLE_EMAIL") 
        self.google_password = os.getenv("GOOGLE_PASSWORD")
        
        if not self.openai_api_key:
            logger.error("Missing OPENAI_API_KEY in environment variables")
            raise ValueError("Missing OpenAI API key")
            
        if not self.google_email or not self.google_password:
            logger.error("Missing GOOGLE_EMAIL or GOOGLE_PASSWORD in environment variables")
            logger.info("Please add your Google credentials to .env file")
            raise ValueError("Missing Google credentials")
        
        # Setup OpenAI
        openai.api_key = self.openai_api_key
        
        # Initialize WebDriver
        self.driver = None
        
        # Blog topics pool
        self.topics = [
            "The future of artificial intelligence in everyday life",
            "How remote work is reshaping the modern workplace",
            "The rise of sustainable technology and green innovation",
            "Digital transformation in healthcare: opportunities and challenges",
            "The evolution of cybersecurity in the digital age",
            "Smart cities: Building the urban future with IoT",
            "Blockchain beyond cryptocurrency: Real-world applications",
            "The psychology of user experience design",
            "Climate tech: Innovations fighting climate change",
            "The gig economy and future of freelance work",
            "Virtual reality applications beyond gaming",
            "Data privacy in the age of big data",
            "Machine learning democratization: AI for everyone",
            "The rise of no-code/low-code development platforms",
            "Social media's impact on mental health and society",
            "Automation and the changing job market landscape",
            "Digital wellness: Finding balance in a connected world",
            "The future of education: Online learning evolution",
            "Quantum computing: The next technological revolution",
            "Sustainable software development practices"
        ]
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options"""
        try:
            chrome_options = Options()
            
            # Set Chrome binary path for macOS
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            
            # Add options for automation
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # For headless mode (comment out to see browser window)
            # chrome_options.add_argument("--headless")
            
            # Try to setup driver with proper Chrome path
            try:
                # Get ChromeDriver path
                driver_path = ChromeDriverManager().install()
                
                # Fix the driver path if it's pointing to wrong file
                if "THIRD_PARTY_NOTICES" in driver_path:
                    import os
                    driver_dir = os.path.dirname(driver_path)
                    # Look for the actual chromedriver executable
                    for file in os.listdir(driver_dir):
                        if file == "chromedriver" and os.access(os.path.join(driver_dir, file), os.X_OK):
                            driver_path = os.path.join(driver_dir, file)
                            break
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                
            except Exception as e:
                logger.warning(f"ChromeDriverManager failed: {e}, trying direct approach...")
                # Fallback: try without explicit service but with binary location
                self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("WebDriver setup successful")
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {str(e)}")
            raise
    
    def login_to_medium(self):
        """Login to Medium using Google authentication"""
        try:
            logger.info("Logging into Medium via Google...")
            
            # Navigate to Medium sign-in page
            self.driver.get("https://medium.com/m/signin")
            time.sleep(3)
            
            # Click on "Continue with Google"
            try:
                google_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue with Google')]"))
                )
                google_button.click()
                time.sleep(3)
            except:
                # Try alternative selectors for Google login
                try:
                    google_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Google')]")
                    google_button.click()
                    time.sleep(3)
                except:
                    # Try finding by partial text or other attributes
                    google_button = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Google')]")
                    google_button.click()
                    time.sleep(3)
            
            # Handle Google login popup/redirect
            # Switch to Google login window if it's a popup
            original_window = self.driver.current_window_handle
            
            # Wait for potential new window/tab
            time.sleep(2)
            
            # Check if we're redirected to Google or if there's a popup
            if "accounts.google.com" in self.driver.current_url:
                # We're on Google login page
                logger.info("Redirected to Google login page")
                
                # Enter Google email
                try:
                    email_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "identifierId"))
                    )
                    email_input.send_keys(self.google_email)
                    
                    # Click Next
                    next_button = self.driver.find_element(By.ID, "identifierNext")
                    next_button.click()
                    time.sleep(3)
                    
                    # Enter password
                    password_input = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.NAME, "password"))
                    )
                    password_input.send_keys(self.google_password)
                    
                    # Click Next/Sign in
                    password_next = self.driver.find_element(By.ID, "passwordNext")
                    password_next.click()
                    time.sleep(5)
                    
                except Exception as e:
                    logger.error(f"Error during Google authentication: {e}")
                    return False
            
            # Wait to be redirected back to Medium
            WebDriverWait(self.driver, 15).until(
                lambda driver: "medium.com" in driver.current_url and "signin" not in driver.current_url
            )
            
            # Check if login was successful
            if "medium.com" in self.driver.current_url and "signin" not in self.driver.current_url:
                logger.info("✅ Successfully logged into Medium via Google")
                return True
            else:
                logger.error("❌ Login to Medium failed")
                return False
                
        except Exception as e:
            logger.error(f"Error logging into Medium: {str(e)}")
            return False
    
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
                        "content": """You are a professional Medium blog writer. Write engaging, informative, and well-structured blog posts optimized for Medium's audience. 

                        Guidelines:
                        - Use compelling storytelling and personal insights
                        - Include practical takeaways and actionable advice
                        - Write in a conversational yet professional tone
                        - Use subheadings to break up content (use ## for subheadings)
                        - Include relevant examples and case studies
                        - Make it 700-900 words for optimal Medium engagement
                        - End with a call-to-action or thought-provoking question"""
                    },
                    {
                        "role": "user", 
                        "content": f"Write a comprehensive Medium blog post about: {topic}. Make it engaging with personal insights, practical examples, and clear takeaways that readers can apply. Use ## for subheadings."
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
                        "content": f"Create one engaging Medium article title for this topic: {topic}. Just return the title, nothing else."
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
    
    def post_to_medium(self, title: str, content: str):
        """Post the blog to Medium using web automation"""
        try:
            logger.info("Creating new Medium story...")
            
            # Navigate to new story page
            self.driver.get("https://medium.com/new-story")
            time.sleep(5)
            
            # Find and click the title area
            title_element = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//h1[@data-default-value='Title']"))
            )
            title_element.click()
            time.sleep(1)
            
            # Clear and enter title
            title_element.clear()
            title_element.send_keys(title)
            time.sleep(2)
            
            # Find the content area
            content_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-default-value='Tell your story…']"))
            )
            content_element.click()
            time.sleep(1)
            
            # Clear and enter content
            content_element.clear()
            content_element.send_keys(content)
            time.sleep(3)
            
            # Add tags
            logger.info("Adding tags...")
            try:
                # Scroll down to find tags section
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Look for tags input
                tags_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Add a tag...']")
                tags = ["technology", "ai", "innovation", "future", "automation"]
                
                for tag in tags[:3]:  # Add first 3 tags
                    tags_input.send_keys(tag)
                    time.sleep(1)
                    # Press Enter to add tag
                    tags_input.send_keys("\n")
                    time.sleep(1)
                    
            except Exception as tag_error:
                logger.warning(f"Could not add tags: {tag_error}")
            
            # Publish the post
            logger.info("Publishing the post...")
            
            # Find and click publish button
            publish_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Publish')]"))
            )
            publish_button.click()
            time.sleep(3)
            
            # Confirm publish
            try:
                confirm_publish = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Publish now')]"))
                )
                confirm_publish.click()
                time.sleep(5)
                
                logger.info("✅ Successfully published to Medium!")
                return True
                
            except TimeoutException:
                logger.warning("Could not find final publish button - post may already be published")
                return True
                
        except Exception as e:
            logger.error(f"Error posting to Medium: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
    
    def run(self):
        """Main execution method"""
        try:
            logger.info("🚀 Starting automated Medium blog posting...")
            
            # Setup WebDriver
            self.setup_driver()
            
            # Login to Medium
            if not self.login_to_medium():
                raise Exception("Failed to login to Medium")
            
            # Select a random topic
            topic = random.choice(self.topics)
            logger.info(f"Selected topic: {topic}")
            
            # Generate blog content
            blog_data = self.generate_blog_content(topic)
            title = blog_data["title"]
            content = blog_data["content"]
            
            logger.info(f"Generated content: {len(content)} characters")
            
            # Post to Medium
            success = self.post_to_medium(title, content)
            
            if success:
                logger.info("✅ Automated blog posting completed successfully!")
                print(f"\n🎉 Successfully Posted to Medium:")
                print(f"📝 Title: {title}")
                print(f"📄 Content: {len(content)} characters")
                print(f"🌐 Check your Medium profile for the published post!")
                
                return {
                    "title": title,
                    "content": content,
                    "success": True
                }
            else:
                raise Exception("Failed to post to Medium")
                
        except Exception as e:
            logger.error(f"❌ Automated blog posting failed: {str(e)}")
            raise
        finally:
            self.cleanup()

if __name__ == "__main__":
    bot = AutoMediumBlogBot()
    bot.run()
