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
    Downloads the PDF and provides a summary.
    """
    ack()
    url = command['text'].strip()
    
    if not url:
        respond("Please provide an arXiv URL to summarize. Usage: `/summarize <arxiv_url>`")
        return

    # Validate it's an arXiv URL
    if 'arxiv.org' not in url:
        respond("Please provide a valid arXiv URL (e.g., https://arxiv.org/abs/1706.03762)")
        return

    respond(f":hourglass: Fetching and summarizing paper from {url}... This may take a moment.")
    
    try:
        # Create paper object - the summarizer will fetch the PDF content
        paper = {
            'title': 'On-Demand Request',
            'abstract': '',
            'link': url
        }
        
        summary = summarizer.summarize(paper)
        respond(f"*Summary for <{url}|paper>:*\n\n{summary}")
    except Exception as e:
        respond(f":x: Error summarizing paper: {str(e)}")

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
