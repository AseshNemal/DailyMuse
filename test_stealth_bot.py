#!/usr/bin/env python3
"""
Enhanced Automated Medium Blog Bot
This version uses improved stealth techniques to avoid detection
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
from selenium.webdriver.common.action_chains import ActionChains

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

class StealthMediumBot:
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
            "The evolution of cybersecurity in the digital age"
        ]
    
    def setup_stealth_driver(self):
        """Setup Chrome WebDriver with advanced stealth options"""
        try:
            chrome_options = Options()
            
            # Basic stealth options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Advanced stealth options
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            
            # Set a realistic user agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Set window size
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Use Chrome binary path for macOS
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            
            # Setup driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            logger.info("Stealth WebDriver setup successful")
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {str(e)}")
            raise
    
    def manual_login_test(self):
        """Test login by opening browser and waiting for manual intervention"""
        try:
            logger.info("Opening Medium login page for manual testing...")
            
            # Navigate to Medium sign-in page
            self.driver.get("https://medium.com/m/signin")
            time.sleep(3)
            
            print("\n" + "="*60)
            print("🔍 MANUAL LOGIN TEST")
            print("="*60)
            print("1. A Chrome browser window has opened")
            print("2. Please manually log in to Medium using Google")
            print("3. Once logged in, press Enter here to continue...")
            print("4. The bot will then try to create a test post")
            print("="*60)
            
            # Wait for user to login manually
            input("Press Enter after you've logged in to Medium...")
            
            # Check if login was successful
            current_url = self.driver.current_url
            if "medium.com" in current_url and "signin" not in current_url:
                logger.info("✅ Login successful! Proceeding with content generation...")
                return True
            else:
                logger.error("❌ Please make sure you're logged in to Medium")
                return False
                
        except Exception as e:
            logger.error(f"Error in manual login test: {str(e)}")
            return False
    
    def generate_simple_content(self):
        """Generate simple test content"""
        try:
            topic = random.choice(self.topics)
            logger.info(f"Generating content for: {topic}")
            
            # Generate simple content for testing
            content_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a blog writer. Write a short, engaging blog post of about 300 words."
                    },
                    {
                        "role": "user", 
                        "content": f"Write a brief blog post about: {topic}"
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = content_response["choices"][0]["message"]["content"]
            
            # Generate title
            title_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Create a catchy blog title. Return only the title."
                    },
                    {
                        "role": "user", 
                        "content": f"Create a title for: {topic}"
                    }
                ],
                max_tokens=50,
                temperature=0.8
            )
            
            title = title_response["choices"][0]["message"]["content"].strip().strip('"')
            
            return {"title": title, "content": content}
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            # Return fallback content for testing
            return {
                "title": "Test Post from DailyMuse Bot",
                "content": "This is a test post generated by the DailyMuse automated blog bot. If you're seeing this, the automation is working!"
            }
    
    def create_medium_post(self, title: str, content: str):
        """Create a new Medium post"""
        try:
            logger.info("Creating new Medium post...")
            
            # Navigate to new story page
            self.driver.get("https://medium.com/new-story")
            time.sleep(5)
            
            # Wait for page to load and find title area
            try:
                # Try different selectors for the title
                title_selectors = [
                    "h1[data-default-value='Title']",
                    "h1[placeholder='Title']",
                    ".graf--title",
                    "h1",
                    "[data-testid='storyTitle']"
                ]
                
                title_element = None
                for selector in title_selectors:
                    try:
                        title_element = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        break
                    except:
                        continue
                
                if not title_element:
                    logger.error("Could not find title element")
                    return False
                
                # Click and enter title
                title_element.click()
                time.sleep(1)
                title_element.clear()
                title_element.send_keys(title)
                time.sleep(2)
                
                logger.info(f"Title entered: {title}")
                
            except Exception as e:
                logger.error(f"Error with title: {str(e)}")
                return False
            
            # Find and fill content area
            try:
                # Try different selectors for content
                content_selectors = [
                    "div[data-default-value='Tell your story…']",
                    ".graf--p",
                    "[data-testid='storyContent']",
                    ".notranslate"
                ]
                
                content_element = None
                for selector in content_selectors:
                    try:
                        content_element = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        break
                    except:
                        continue
                
                if content_element:
                    content_element.click()
                    time.sleep(1)
                    content_element.send_keys(content)
                    time.sleep(3)
                    logger.info("Content entered successfully")
                else:
                    logger.warning("Could not find content area - trying manual approach")
                    print("\n" + "="*50)
                    print("⚠️ MANUAL CONTENT ENTRY NEEDED")
                    print("="*50)
                    print("Please manually add this content to the Medium post:")
                    print(f"Title: {title}")
                    print(f"Content: {content}")
                    print("="*50)
                    input("Press Enter after adding the content...")
                
            except Exception as e:
                logger.error(f"Error with content: {str(e)}")
            
            # Ask user if they want to publish
            print("\n" + "="*50)
            print("📝 POST READY")
            print("="*50)
            print("The post has been created in Medium.")
            print("You can now:")
            print("1. Review the post")
            print("2. Add tags if needed") 
            print("3. Publish manually")
            print("="*50)
            
            publish = input("Do you want the bot to try to publish automatically? (y/n): ").lower().strip()
            
            if publish == 'y':
                try:
                    # Try to find and click publish button
                    publish_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Publish') or contains(text(), 'Share')]"))
                    )
                    publish_button.click()
                    time.sleep(3)
                    
                    # Confirm publish if needed
                    try:
                        confirm_publish = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Publish now')]"))
                        )
                        confirm_publish.click()
                        time.sleep(3)
                        logger.info("✅ Post published successfully!")
                    except:
                        logger.info("✅ Post created successfully (manual publish may be needed)")
                    
                    return True
                    
                except Exception as e:
                    logger.error(f"Could not auto-publish: {str(e)}")
                    logger.info("Please publish manually")
                    return True
            else:
                logger.info("✅ Post created successfully - publish manually when ready")
                return True
                
        except Exception as e:
            logger.error(f"Error creating Medium post: {str(e)}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            input("Press Enter to close the browser...")
            self.driver.quit()
            logger.info("Browser closed")
    
    def run_test(self):
        """Run the test with manual assistance"""
        try:
            logger.info("🚀 Starting Medium posting test...")
            
            # Setup browser
            self.setup_stealth_driver()
            
            # Manual login test
            if not self.manual_login_test():
                raise Exception("Login failed")
            
            # Generate content
            blog_data = self.generate_simple_content()
            title = blog_data["title"]
            content = blog_data["content"]
            
            # Create post
            success = self.create_medium_post(title, content)
            
            if success:
                logger.info("✅ Test completed successfully!")
                print(f"\n🎉 SUCCESS!")
                print(f"📝 Title: {title}")
                print(f"📄 Content: {len(content)} characters")
                return True
            else:
                logger.error("❌ Test failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
            return False
        finally:
            self.cleanup()

if __name__ == "__main__":
    print("🤖 DailyMuse Medium Bot - Interactive Test")
    print("=" * 50)
    print("This test will:")
    print("1. Open a browser")
    print("2. Let you login manually to Medium")
    print("3. Generate AI content")
    print("4. Create a Medium post")
    print("5. Optionally publish it")
    print("=" * 50)
    
    bot = StealthMediumBot()
    bot.run_test()
