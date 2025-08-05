#!/usr/bin/env python3
"""
Manual trigger for daily automation - Test locally before GitHub Actions
"""

import os
import subprocess
import sys
from datetime import datetime

def test_daily_automation():
    """Test the daily automation locally"""
    
    print("🧪 Testing Daily Automation Locally")
    print("=" * 40)
    print(f"📅 Test run at: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print()
    
    # Check if all required files exist
    required_files = [
        'oauth_blogger_bot.py',
        'credentials.json', 
        'token.pickle',
        '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found {file}")
        else:
            print(f"❌ Missing {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Cannot run automation. Missing files: {', '.join(missing_files)}")
        return False
    
    print("\n🚀 Running automated blog posting...")
    print("─" * 40)
    
    try:
        # Run the OAuth blogger bot
        result = subprocess.run([
            sys.executable, 'oauth_blogger_bot.py'
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ AUTOMATION TEST SUCCESSFUL!")
            print("🎉 Your daily automation is working correctly")
            print("🚀 Ready to deploy to GitHub Actions")
            return True
        else:
            print(f"\n❌ AUTOMATION TEST FAILED (Exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Error running automation: {e}")
        return False

def show_github_setup_reminder():
    """Show reminder about GitHub setup"""
    
    print("\n" + "🎯 GITHUB ACTIONS SETUP REMINDER")
    print("=" * 50)
    print("1. Go to: https://github.com/AseshNemal/DailyMuse")
    print("2. Settings → Secrets and variables → Actions")
    print("3. Add all secrets from 'github_secrets.txt'")
    print("4. Go to Actions tab → Run 'Daily AI Blog Generation' workflow")
    print("5. Your blog will auto-post daily at 9:00 AM UTC")
    print()
    print("🌐 Your blog: https://dailymuset.blogspot.com")

if __name__ == "__main__":
    print("🤖 DailyMuse Daily Automation Test")
    print("This will test your automation before deploying to GitHub\n")
    
    success = test_daily_automation()
    
    if success:
        show_github_setup_reminder()
        print("\n🎉 Everything is ready for daily automation!")
    else:
        print("\n❌ Fix the issues above before setting up GitHub Actions")
