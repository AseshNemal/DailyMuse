# DailyMuse 🚀
**Automated AI-Powered Blog Posting to Medium**

[![Daily Blog Post](https://github.com/AseshNemal/DailyMuse/actions/workflows/daily-blog.yml/badge.svg)](https://github.com/AseshNemal/DailyMuse/actions/workflows/daily-blog.yml)

An intelligent, fully automated system that generates AI-written blog posts with AI-generated images and publishes them directly to Medium using the Medium API. This project leverages OpenAI's GPT-3.5 for content generation and DALL·E for image creation, running seamlessly on GitHub Actions with daily scheduling.

## ✨ Features

- 🤖 **AI Content Generation**: Uses OpenAI GPT-3.5 to create engaging, well-structured blog posts
- 🎨 **Smart Image Generation**: DALL·E integration for relevant visual content (cost-optimized to run every other day)
- 📝 **Automatic Publishing**: Direct posting to Medium via official API
- ⏰ **Scheduled Automation**: GitHub Actions workflow runs daily at 9:00 AM UTC
- 💰 **Cost Optimized**: Strategic AI usage to minimize costs while maintaining quality
- 🏷️ **Auto-tagging**: Automatically adds relevant tags to blog posts
- 📊 **Comprehensive Logging**: Detailed logging for monitoring and debugging
- 🔐 **Secure**: API keys stored safely as GitHub secrets

## 🏗️ Project Structure

```
DailyMuse/
├── auto-medium-blog/
│   ├── blog_bot.py          # Main bot logic
│   └── requirements.txt     # Python dependencies
├── .github/workflows/
│   └── daily-blog.yml      # GitHub Actions workflow
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/AseshNemal/DailyMuse.git
cd DailyMuse
```

### 2. Install Dependencies
```bash
cd auto-medium-blog
pip install -r requirements.txt
```

### 3. Set Up API Keys

#### Get OpenAI API Key
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key for later use

#### Get Medium Integration Token
1. Go to [Medium Settings](https://medium.com/me/settings)
2. Scroll to "Integration tokens"
3. Create a new integration token
4. Copy the token for later use

### 4. Configure GitHub Secrets
In your GitHub repository, go to Settings → Secrets and variables → Actions:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MEDIUM_TOKEN`: Your Medium integration token

### 5. Test Locally (Optional)
```bash
export OPENAI_API_KEY="your-openai-api-key"
export MEDIUM_TOKEN="your-medium-token"
cd auto-medium-blog
python blog_bot.py
```

## 🤖 How It Works

### Content Generation Process
1. **Topic Selection**: Randomly selects from a curated list of 20+ technology and innovation topics
2. **Content Creation**: Uses GPT-3.5 to generate comprehensive 600-800 word blog posts
3. **Title Generation**: Creates engaging, click-worthy titles using AI
4. **Image Generation**: On alternate days, generates relevant images using DALL·E
5. **HTML Formatting**: Formats content with proper HTML structure and styling
6. **Publishing**: Posts directly to Medium with appropriate tags

### Cost Optimization Strategy
- **Image Generation**: Alternates days to reduce DALL·E usage costs
- **Efficient Prompting**: Optimized prompts to minimize token usage
- **GitHub Actions**: Leverages free GitHub Actions minutes
- **Smart Scheduling**: Single daily execution prevents excessive API calls

## 📊 Bot Capabilities

### Content Topics
The bot covers diverse technology topics including:
- Artificial Intelligence & Machine Learning
- Remote Work & Digital Transformation
- Cybersecurity & Data Privacy
- Sustainable Technology
- Healthcare Innovation
- Blockchain & Cryptocurrency
- Social Media Impact
- Future of Work
- Smart Cities & IoT
- And many more...

### Content Quality Features
- Professional writing tone
- Structured format (introduction, body, conclusion)
- Real-world examples and practical insights
- SEO-optimized titles
- Relevant tagging for Medium's algorithm
- Publication date and AI attribution

## 🔧 Configuration

### Customizing Topics
Edit the `topics` list in `blog_bot.py` to add your preferred subjects:

```python
self.topics = [
    "Your custom topic here",
    "Another interesting topic",
    # ... add more topics
]
```

### Adjusting Schedule
Modify the cron expression in `.github/workflows/daily-blog.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Daily at 9:00 AM UTC
```

### Image Generation Frequency
Change the image generation logic in the `should_use_image()` method:

```python
def should_use_image(self) -> bool:
    # Current: every other day
    day_of_year = datetime.now().timetuple().tm_yday
    return day_of_year % 2 == 0
```

## 📈 Monitoring & Logs

### GitHub Actions Logs
- View execution logs in the Actions tab of your repository
- Monitor success/failure status
- Debug any issues with detailed logging

### Bot Logging
The bot provides comprehensive logging:
- Topic selection
- Content generation status
- Image generation decisions
- Medium posting results
- Error handling and debugging info

## 🛠️ Troubleshooting

### Common Issues

**Authentication Errors**
- Verify API keys are correctly set in GitHub secrets
- Check Medium token permissions
- Ensure OpenAI account has sufficient credits

**Content Generation Failures**
- Check OpenAI API quota and billing
- Verify internet connectivity in GitHub Actions
- Review error logs for specific issues

**Medium Publishing Issues**
- Confirm Medium token is valid and active
- Check Medium API rate limits
- Verify account permissions for posting

### Debug Mode
For local testing, add debug logging:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 💡 Future Enhancements

- [ ] Multiple platform support (LinkedIn, Dev.to, etc.)
- [ ] Advanced content personalization
- [ ] Performance analytics and metrics
- [ ] Custom image styles and branding
- [ ] A/B testing for titles and content
- [ ] Integration with content calendar
- [ ] Webhook notifications for successful posts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project is for educational and personal use. Please ensure compliance with:
- Medium's Terms of Service
- OpenAI's Usage Policies
- GitHub's Terms of Service
- Applicable content creation guidelines

## 🙏 Acknowledgments

- OpenAI for GPT-3.5 and DALL·E APIs
- Medium for their publishing platform and API
- GitHub for Actions and hosting
- The open-source community for inspiration

---

**Made with ❤️ and AI** | [Follow me on Medium](https://medium.com/@your-medium-handle) 
# Test deployment trigger
