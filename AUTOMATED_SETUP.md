# 🤖 Automated Medium Posting Setup Guide

## Prerequisites

### 1. Install Required Dependencies
```bash
pip3 install selenium==4.15.2 webdriver-manager==4.0.1
```

### 2. Set Up Your Environment Variables

Edit your `.env` file with your Google credentials:

```env
# DailyMuse Environment Variables
OPENAI_API_KEY=your-openai-key-here

# Google Login Credentials (for Medium via Google)
GOOGLE_EMAIL=aseshnemal@gmail.com
GOOGLE_PASSWORD=your-google-password-here
```

⚠️ **Important Security Notes:**
- Use an App Password if you have 2FA enabled on Google
- Consider creating a dedicated Google account for automation
- Never commit the `.env` file to git

## 🚀 How to Use

### Option 1: Run Locally
```bash
cd /Users/aseshnemal/Desktop/app/DailyMuse
python3 auto_medium_bot.py
```

### Option 2: Test First
```bash
# Install dependencies
pip3 install -r auto-medium-blog/requirements.txt

# Test the bot
python3 auto_medium_bot.py
```

## 🔧 Setup Steps

### 1. Fix OpenAI Credits
- Go to https://platform.openai.com/account/billing
- Add payment method and credits ($5-10 is usually enough)

### 2. Set Up Google Authentication
- Add your Google email to `.env`
- Add your Google password to `.env`
- If you have 2FA, you'll need an App Password:
  1. Go to Google Account settings
  2. Security → 2-Step Verification → App passwords
  3. Generate password for "Mail" or "Other"
  4. Use this password in `.env`

### 3. Test the Bot
```bash
python3 auto_medium_bot.py
```

## 🤔 Troubleshooting

### Common Issues:

1. **Chrome Driver Issues**
   - The script auto-downloads ChromeDriver
   - Make sure Chrome browser is installed

2. **Google Login Problems**
   - Check if 2FA is enabled (use App Password)
   - Verify email/password are correct
   - Google may block automated logins sometimes

3. **Medium Posting Issues**
   - Check if you're logged into Medium manually first
   - Medium may have changed their interface
   - Try running in non-headless mode to see what's happening

### Debug Mode
To see what's happening, modify the Chrome options in `auto_medium_bot.py`:
```python
# Comment out this line to see the browser
# chrome_options.add_argument("--headless")
```

## 🔄 Alternative Approaches

If automated posting doesn't work reliably:

### 1. Semi-Automated (Recommended)
- Use `medium_ready_bot.py` to generate content
- Manually copy-paste to Medium
- Still saves time on content creation

### 2. Scheduled Generation Only
- Generate posts daily via GitHub Actions
- Download and post manually when convenient

## 📋 Daily Workflow

Once set up:
1. Bot runs automatically (via GitHub Actions or local cron)
2. Generates AI content
3. Logs into Medium via Google
4. Posts content with tags
5. Logs success/failure

## 🛡️ Security Best Practices

- Use App Passwords instead of main Google password
- Consider a dedicated Google account for automation
- Regularly rotate passwords
- Monitor for unusual account activity
- Keep `.env` file in `.gitignore`

## 📞 Need Help?

- Check logs for specific error messages
- Test manual Google login to Medium first
- Verify all environment variables are set
- Try running in debug mode (non-headless)

Happy automated blogging! 🚀
