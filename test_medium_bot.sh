#!/bin/bash

echo "🚀 Testing Medium-Ready Blog Bot"
echo "================================"

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ OpenAI API key not found in environment"
    echo "Make sure to set it in your .env file"
    echo ""
fi

# Run the Medium-ready bot
echo "📝 Generating Medium-ready blog post..."
python3 medium_ready_bot.py

# Check if any markdown files were created
if ls medium_post_*.md 1> /dev/null 2>&1; then
    echo ""
    echo "✅ Success! Generated files:"
    ls -la medium_post_*.md
    echo ""
    echo "📋 Next steps:"
    echo "1. Open the generated .md file"
    echo "2. Copy the content"
    echo "3. Go to https://medium.com/new-story"
    echo "4. Paste and format your post"
    echo "5. Add tags and publish!"
else
    echo "❌ No blog posts were generated"
    echo "Check the error messages above"
fi
