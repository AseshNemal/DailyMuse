#!/usr/bin/env python3
"""
Simple test to see Medium login page and identify elements
"""

import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
        print("Environment variables loaded from .env file")

def test_medium_login():
    """Test Medium login page interaction"""
    load_env()
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    # Don't run headless so we can see what's happening
    # chrome_options.add_argument("--headless")
    
    try:
        # Setup driver
        driver = webdriver.Chrome(options=chrome_options)
        
        print("🚀 Opening Medium login page...")
        driver.get("https://medium.com/m/signin")
        
        print("⏳ Waiting 10 seconds for you to see the page...")
        time.sleep(10)
        
        print("📱 Looking for login options...")
        
        # Try to find different login elements
        page_source = driver.page_source
        
        if "Continue with Google" in page_source:
            print("✅ Found 'Continue with Google' text in page")
        
        if "Sign in with Google" in page_source:
            print("✅ Found 'Sign in with Google' text in page")
            
        if "Google" in page_source:
            print("✅ Found 'Google' text somewhere in page")
        
        # Save page source for analysis
        with open("medium_login_page.html", "w") as f:
            f.write(page_source)
        print("💾 Saved page source to medium_login_page.html")
        
        print("⏳ Keeping browser open for 30 seconds so you can inspect...")
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("✅ Browser closed")

if __name__ == "__main__":
    test_medium_login()
