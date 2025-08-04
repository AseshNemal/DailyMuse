# DailyMuse Configuration
# Customize these settings to personalize your automated blog

# Blog Configuration
BLOG_TAGS = ["technology", "ai", "innovation", "future", "automation"]
POST_STATUS = "public"  # Options: "public", "draft", "unlisted"

# Content Settings
MIN_WORDS = 600
MAX_WORDS = 800
CONTENT_TEMPERATURE = 0.7  # OpenAI creativity (0.0 to 1.0)
TITLE_TEMPERATURE = 0.8

# Image Settings
IMAGE_SIZE = "1024x1024"  # Options: "256x256", "512x512", "1024x1024"
IMAGE_FREQUENCY = "alternate"  # Options: "daily", "alternate", "weekly", "never"

# Scheduling (for GitHub Actions)
# Format: minute hour day month weekday
# Default: "0 9 * * *" (9:00 AM UTC daily)
CRON_SCHEDULE = "0 9 * * *"

# Advanced Settings
MAX_RETRIES = 3
REQUEST_TIMEOUT = 30
LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR"
