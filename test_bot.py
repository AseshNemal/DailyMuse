#!/usr/bin/env python3
"""
Test script for DailyMuse Blog Bot
Run this to test your configuration before enabling automation
"""

import os
import sys
from datetime import datetime

# Add the auto-medium-blog directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'auto-medium-blog'))

from blog_bot import MediumBlogBot

def test_api_keys():
    """Test if API keys are configured"""
    print("🔐 Testing API key configuration...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    medium_token = os.getenv("MEDIUM_TOKEN")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    if not medium_token:
        print("❌ MEDIUM_TOKEN not found in environment variables")
        return False
    
    print("✅ API keys found in environment")
    return True

def test_content_generation():
    """Test content generation without posting"""
    print("\n📝 Testing content generation...")
    
    try:
        bot = MediumBlogBot()
        
        # Test topic selection
        topic = "Test: The future of automated content creation"
        print(f"Selected topic: {topic}")
        
        # Test content generation
        blog_data = bot.generate_blog_content(topic)
        print(f"✅ Generated title: {blog_data['title']}")
        print(f"✅ Generated content ({len(blog_data['content'])} characters)")
        
        # Test image generation (optional)
        if bot.should_use_image():
            print("📸 Testing image generation...")
            image_url = bot.generate_image(topic)
            if image_url:
                print(f"✅ Generated image: {image_url}")
            else:
                print("⚠️ Image generation failed (this is optional)")
        else:
            print("📝 Skipping image generation (text-only day)")
        
        return True
        
    except Exception as e:
        print(f"❌ Content generation failed: {str(e)}")
        return False

def test_medium_connection():
    """Test Medium API connection"""
    print("\n🔗 Testing Medium API connection...")
    
    try:
        bot = MediumBlogBot()
        user_id = bot.get_medium_user_id()
        print(f"✅ Connected to Medium. User ID: {user_id}")
        return True
        
    except Exception as e:
        print(f"❌ Medium connection failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 DailyMuse Blog Bot Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: API Keys
    if test_api_keys():
        tests_passed += 1
    
    # Test 2: Content Generation
    if test_content_generation():
        tests_passed += 1
    
    # Test 3: Medium Connection
    if test_medium_connection():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your bot is ready for automation.")
        print("\n💡 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Set up GitHub secrets (OPENAI_API_KEY, MEDIUM_TOKEN)")
        print("3. Enable GitHub Actions in your repository")
        print("4. Your bot will start posting daily at 9:00 AM UTC")
    else:
        print("⚠️ Some tests failed. Please fix the issues before enabling automation.")
        print("\n🔧 Troubleshooting:")
        print("- Check your API keys are correct")
        print("- Ensure you have OpenAI credits")
        print("- Verify Medium token permissions")
        print("- Check your internet connection")

if __name__ == "__main__":
    main()
