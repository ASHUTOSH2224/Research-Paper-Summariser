import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Slack Credentials
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# LLM Credentials
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Keeping this if you want to switch back
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o") # Using gpt-4o as suggested default (users can change to mini)

# Monitor Configuration
MONITOR_INTERVAL_MINUTES = int(os.getenv("MONITOR_INTERVAL_MINUTES", 60))
ARXIV_QUERY = os.getenv("ARXIV_QUERY", "cat:cs.AI OR cat:cs.LG OR cat:cs.CL") # Default to AI/ML
MAX_PAPERS_PER_RUN = int(os.getenv("MAX_PAPERS_PER_RUN", 5))

# Storage
DB_PATH = "seen_papers.json"
