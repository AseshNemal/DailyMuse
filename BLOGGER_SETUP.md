# 🚀 Blogger API Setup Guide

## Step 1: Create a Blogger Blog

1. **Go to Blogger**: https://www.blogger.com/
2. **Sign in** with your Google account (aseshnemal@gmail.com)
3. **Create a new blog**:
   - Click "Create New Blog"
   - Choose a title (e.g., "Daily AI Insights")
   - Choose a URL (e.g., daily-ai-insights.blogspot.com)
   - Select a theme
   - Click "Create blog!"

## Step 2: Get Your Blog ID

1. **Go to your Blogger dashboard**
2. **Click on your blog**
3. **Go to Settings** → **Basic**
4. **Find "Blog ID"** in the settings (it's a long number)
5. **Copy this ID** - you'll need it for the `.env` file

## Step 3: Get Blogger API Key

1. **Go to Google Cloud Console**: https://console.developers.google.com/
2. **Create a new project** (or use existing):
   - Click "Create Project"
   - Name it "DailyMuse"
   - Click "Create"
3. **Enable Blogger API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Blogger API v3"
   - Click on it and click "Enable"
4. **Create API Key**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the API key
   - (Optional) Click "Restrict Key" and select "Blogger API" for security

## Step 4: Update Your .env File

```env
# DailyMuse Environment Variables
OPENAI_API_KEY=your-openai-key-here

# Blogger API Configuration  
BLOGGER_API_KEY=your-blogger-api-key-from-step-3
BLOGGER_BLOG_ID=your-blog-id-from-step-2
```

## Step 5: Test the Bot

```bash
cd /Users/aseshnemal/Desktop/app/DailyMuse
python3 blogger_bot.py
```

## 🎯 What the Bot Does

1. **Generates AI content** using OpenAI
2. **Creates engaging titles** optimized for blogs
3. **Formats content** with HTML styling
4. **Posts automatically** to your Blogger blog
5. **Adds tags** and metadata
6. **Returns the published URL**

## 🔧 Troubleshooting

### Common Issues:

1. **"Invalid API Key"**
   - Double-check your API key in `.env`
   - Make sure Blogger API is enabled in Google Cloud

2. **"Blog not found"**
   - Verify your Blog ID is correct
   - Make sure the blog exists and is accessible

3. **"Quota exceeded"** (OpenAI)
   - Add billing to your OpenAI account
   - Check your usage at https://platform.openai.com/usage

### Finding Your Blog ID:
If you can't find the Blog ID in settings:
1. Go to your blog's homepage
2. View page source (Ctrl+U or Cmd+U)
3. Search for "blogId" - you'll find it in the code

## 🚀 Benefits of Blogger vs Medium

✅ **Official API** - No blocking or restrictions
✅ **Free forever** - No paid plans needed  
✅ **Google SEO** - Great search visibility
✅ **Reliable** - Owned by Google
✅ **Customizable** - Full control over design
✅ **Analytics** - Built-in Google Analytics
✅ **Domain** - Can use custom domain

## 📅 Daily Automation

Once set up, the bot will:
- Generate unique AI content daily
- Post automatically to your blog
- Include proper formatting and tags
- Provide publishing confirmation
- Work reliably without browser issues

Ready to test? Just update your `.env` file and run:
```bash
python3 blogger_bot.py
```

🎉 Happy automated blogging!
