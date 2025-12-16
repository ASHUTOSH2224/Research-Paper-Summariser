import os
from slack_bolt import App
import config
from summarizer import Summarizer

# Initialize App
app = App(token=config.SLACK_BOT_TOKEN)
summarizer = Summarizer()

@app.command("/summarize")
def handle_summarize(ack, respond, command):
    """
    Handle /summarize <url> command.
    """
    ack()
    url = command['text'].strip()
    
    if not url:
        respond("Please provide a URL to summarize. Usage: `/summarize <url>`")
        return

    respond(f"Fetching and summarizing {url}...")
    
    # Ideally, we would fetch the paper content here. 
    # For this MVP, we will try to pass the URL to the summarizer or create a minimal paper object.
    # Future improvement: Add 'fetch_paper_from_url' in monitor.py
    
    paper = {
        'title': 'On-Demand Request',
        'abstract': f'Paper located at {url}',
        'link': url
    }
    
    summary = summarizer.summarize(paper)
    respond(f"*Summary for {url}:*\n{summary}")

def post_paper_to_slack(paper):
    """
    Post a paper summary to the configured Slack channel.
    """
    if not config.SLACK_CHANNEL_ID:
        print("SLACK_CHANNEL_ID not configured.")
        return

    print(f"Summarizing and posting: {paper['title']}")
    summary = summarizer.summarize(paper)
    
    try:
        # Use simple text format for maximum width (Native Slack look)
        # Title as Bold, followed by summary, followed by link
        message_text = f"*{paper['title']}*\n\n{summary}\n\n<{paper['link']}|View Original Paper>"

        app.client.chat_postMessage(
            channel=config.SLACK_CHANNEL_ID,
            text=message_text,
            unfurl_links=False
        )
    except Exception as e:
        print(f"Failed to post to Slack: {e}")
