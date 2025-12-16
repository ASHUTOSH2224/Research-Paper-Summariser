import os
import ssl
import certifi
# Patch SSL context to allow unverified HTTPS (fix for macOS python env issues)
ssl._create_default_https_context = ssl._create_unverified_context

from dotenv import load_dotenv
import config
from bot import post_paper_to_slack

# Load env vars
load_dotenv()

def test_slack_flow():
    print("--- 1. Checking Configuration ---")
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")
    
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN not found!")
        return
    if not channel_id:
        print("❌ SLACK_CHANNEL_ID not found!")
        return
        
    print("✅ Slack Configuration found.")

    print("\n--- 2. Preparing Dummy Paper ---")
    dummy_paper = {
        'title': 'Test Paper: Autonomous Research Agent',
        'abstract': 'This is a test paper to verify the Slack integration of the autonomous research agent using OpenAI for summarization.',
        'link': 'https://example.com/test-paper'
    }

    print("\n--- 3. Posting to Slack ---")
    print(f"Target Channel: {channel_id}")
    
    try:
        post_paper_to_slack(dummy_paper)
        print("✅ Attempted to post to Slack. Check your channel!")
    except Exception as e:
        print(f"❌ Failed to post: {e}")

if __name__ == "__main__":
    test_slack_flow()
