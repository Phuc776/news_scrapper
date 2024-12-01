import time
import schedule
from utils.logger import AppLog
from clustering import run_clustering 

def job():
    AppLog.info("Running scheduled clustering task...")
    run_clustering()

if __name__ == "__main__":
    # Run the job once at the start
    AppLog.info("Running initial clustering task...")
    job()

    # Schedule the job to run every day
    schedule.every().day.do(job)
   
    AppLog.info("Scheduler started. Waiting for next scheduled task...")
    
    # Main loop to keep the container running
    while True:
        schedule.run_pending()
        time.sleep(1)