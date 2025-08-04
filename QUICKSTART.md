# 🚀 DailyMuse Quick Start Guide

## 1. Get Your API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy and save the key

### Medium Integration Token
1. Go to https://medium.com/me/settings
2. Scroll to "Integration tokens"
3. Enter description: "DailyMuse Blog Bot"
4. Click "Get integration token"
5. Copy and save the token

## 2. Local Setup (Optional)

```bash
# Run the setup script
./setup.sh

# Set environment variables
export OPENAI_API_KEY="your-openai-key-here"
export MEDIUM_TOKEN="your-medium-token-here" 

# Test the bot
python test_bot.py

# Run manually (optional)
cd auto-medium-blog && python blog_bot.py
```

## 3. GitHub Setup

### Add Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add these secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `MEDIUM_TOKEN`: Your Medium integration token

### Enable Actions
1. Go to Actions tab in your repository
2. Enable GitHub Actions if prompted
3. The workflow will automatically run daily at 9:00 AM UTC

## 4. Monitor & Customize

### View Logs
- Check the Actions tab for execution logs
- Monitor success/failure of daily posts

### Customize Content
- Edit `auto-medium-blog/blog_bot.py` to modify topics
- Update `config.py` for settings
- Adjust `.github/workflows/daily-blog.yml` for scheduling

## 🎉 That's it!

Your AI blog bot will now:
- ✅ Generate unique blog posts daily
- ✅ Create AI images every other day
- ✅ Post automatically to Medium
- ✅ Add relevant tags and formatting
- ✅ Log all activities for monitoring

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Run `python test_bot.py` to diagnose issues
- Review GitHub Actions logs for errors
- Ensure API keys are valid and have sufficient credits

**Happy blogging! 🚀**
