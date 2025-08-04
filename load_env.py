#!/usr/bin/env python3
"""
Environment loader for DailyMuse
This script loads environment variables from .env file
"""

import os
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'
    
    if not env_path.exists():
        print("❌ .env file not found!")
        return False
    
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
    
    return True

if __name__ == "__main__":
    if load_env():
        print("✅ Environment variables loaded from .env file")
        
        # Check if keys are loaded
        openai_key = os.getenv("OPENAI_API_KEY")
        medium_token = os.getenv("MEDIUM_TOKEN")
        
        if openai_key and openai_key != "your-openai-key-here":
            print(f"✅ OpenAI API key loaded: {openai_key[:10]}...")
        else:
            print("⚠️ OpenAI API key not set")
            
        if medium_token and medium_token != "your-medium-token-here":
            print(f"✅ Medium token loaded: {medium_token[:10]}...")
        else:
            print("⚠️ Medium token not set - please get it from https://medium.com/me/settings")
    else:
        print("❌ Failed to load environment variables")
