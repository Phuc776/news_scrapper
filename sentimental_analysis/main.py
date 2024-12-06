import time
import schedule
from utils.logger import AppLog
from sentimental import run_sentiment_analysis
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

async def job():
    AppLog.info("Running scheduled sentiment analysis task...")
    run_sentiment_analysis()

async def periodic_sentimental():
    """This function will be called every day to run the sentimental task"""
    while True:
        await job()
        await asyncio.sleep(300)  

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    sentimental_task = asyncio.create_task(periodic_sentimental())
    try:
        yield  
    finally:
        sentimental_task.cancel()  
        try:
            await sentimental_task
        except asyncio.CancelledError:
            AppLog.error("Sentimental task is cancelled")
            pass


app = FastAPI(lifespan=app_lifespan)

@app.get("/sentimental")
async def sentimental_data_api():
    await job()
    return {"message": "Setimental data triggered successfully"}

@app.get("/")
def home():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)