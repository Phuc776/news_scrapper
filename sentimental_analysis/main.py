import time
import schedule
from utils.logger import AppLog
from sentimental_analysis.sentimental import run_sentiment_analysis

def job():
    AppLog.info("Running scheduled sentiment analysis task...")
    run_sentiment_analysis()

if __name__ == "__main__":
    # Run the job once at the start
    AppLog.info("Running initial sentiment analysis task...")
    job()

    # Schedule the job to run every day
    schedule.every().day.do(job)

    AppLog.info("Scheduler started. Waiting for next scheduled task...")

    # Main loop to keep the container running
    while True:
        schedule.run_pending()
        time.sleep(1)
