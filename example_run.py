#!/usr/bin/env python3
"""
Example usage of the DailyMuse Blog Bot
This demonstrates how to use the bot programmatically
"""

import os
import sys
from datetime import datetime

# Add the auto-medium-blog directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
blog_dir = os.path.join(current_dir, 'auto-medium-blog')
sys.path.insert(0, blog_dir)

def run_example():
    """Example of running the blog bot with custom settings"""
    
    print("🚀 DailyMuse Blog Bot - Example Run")
    print("=" * 50)
    
    # Check if environment variables are set
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("MEDIUM_TOKEN"):
        print("⚠️ Missing API keys!")
        print("Please set the following environment variables:")
        print("- OPENAI_API_KEY")
        print("- MEDIUM_TOKEN")
        print("\nExample:")
        print("export OPENAI_API_KEY='your-key-here'")
        print("export MEDIUM_TOKEN='your-token-here'")
        return
    
    try:
        # Import the bot (after adding to path)
        from blog_bot import MediumBlogBot
        
        # Create and run the bot
        bot = MediumBlogBot()
        result = bot.run()
        
        print("\n🎉 Success!")
        print(f"Blog URL: {result.get('url', 'N/A')}")
        print(f"Post ID: {result.get('id', 'N/A')}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the correct directory and have installed dependencies.")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        print("Check your API keys and internet connection.")

if __name__ == "__main__":
    run_example()
