#!/bin/bash

# DailyMuse Setup Script
# This script helps you set up the project for local development

echo "🚀 Setting up DailyMuse - Automated Blog Bot"
echo "============================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r auto-medium-blog/requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🔑 Next steps:"
echo "1. Set up your environment variables:"
echo "   export OPENAI_API_KEY='your-openai-api-key'"
echo "   export MEDIUM_TOKEN='your-medium-token'"
echo ""
echo "2. Test your setup:"
echo "   python test_bot.py"
echo ""
echo "3. Run the bot manually:"
echo "   cd auto-medium-blog && python blog_bot.py"
echo ""
echo "📚 For more information, see README.md"
