from apscheduler.schedulers.background import BackgroundScheduler
from slack_bolt.adapter.socket_mode import SocketModeHandler
import ssl
import certifi

# Patch SSL context for macOS
ssl._create_default_https_context = ssl._create_unverified_context

import config
from monitor import ResearchMonitor
from bot import app, post_paper_to_slack
import time

def monitor_job():
    print("--- [Job Start] Running Research Monitor ---")
    monitor = ResearchMonitor()
    new_papers = monitor.fetch_arxiv_papers()
    print(f"Found {len(new_papers)} new papers.")
    
    for paper in new_papers:
        post_paper_to_slack(paper)
        time.sleep(2) # Prevent spamming
    print("--- [Job End] ---")

def main():
    # 1. Start Scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(monitor_job, 'interval', minutes=config.MONITOR_INTERVAL_MINUTES)
    scheduler.start()
    print(f"Scheduler started. Monitor runs every {config.MONITOR_INTERVAL_MINUTES} minutes.")

    # Optional: Run once on startup to verify
    monitor_job()

    # 2. Start Slack Bot
    if config.SLACK_APP_TOKEN and config.SLACK_BOT_TOKEN:
        print("Starting Slack Socket Mode Handler...")
        try:
            handler = SocketModeHandler(app, config.SLACK_APP_TOKEN)
            handler.start()
        except Exception as e:
            print(f"Error starting Slack Bot: {e}")
    else:
        print("WARNING: Slack tokens not set in .env. Bot will not run.")
        # If no bot, keep the script running for the scheduler
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
