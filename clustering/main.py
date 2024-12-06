from utils.logger import AppLog
from clustering import run_clustering 
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

async def job():
    AppLog.info("Running scheduled clustering task...")
    run_clustering()

async def periodic_clustering():
    """This function will be called every day to run the clustering task"""
    while True:
        await job()
        await asyncio.sleep(86400)  # 86400 seconds = 1 day

# Lifespan Context Manager
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    clustering_task = asyncio.create_task(periodic_clustering())
    try:
        yield  
    finally:
        clustering_task.cancel()  
        try:
            await clustering_task
        except asyncio.CancelledError:
            AppLog.error("CLustering task is cancelled")
            pass


app = FastAPI(lifespan=app_lifespan)

@app.get("/clustering")
async def clustering_data_api():
    await job()
    return {"message": "Clustering data triggered successfully"}

@app.get("/")
def home():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)