import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from news_scraping import get_raw_data, insert_to_db
from utils.logger import AppLog

async def crawl_data():
    """Crawl data from news websites and insert to database"""
    try:
        articles_data = get_raw_data()  # Assuming get_raw_data is an async function
        insert_to_db(articles_data)  # Assuming insert_to_db is an async function
    except Exception as e:
        AppLog.error(f"Error while crawling data: {e}")


async def periodic_crawl():
    """This function will be called every 5 minutes"""
    while True:
        await crawl_data()
        await asyncio.sleep(300)  # Wait for 5 minutes

# Lifespan Context Manager
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    crawler_task = asyncio.create_task(periodic_crawl())
    try:
        yield  
    finally:
        crawler_task.cancel()  
        try:
            await crawler_task
        except asyncio.CancelledError:
            AppLog.error("Crawler task is cancelled")
            pass

app = FastAPI(lifespan=app_lifespan)

@app.get("/crawl")
async def crawl_data_api():
    await crawl_data()
    return {"message": "Crawl data triggered successfully"}

@app.get("/")
def home():
    return {"message": "Hello, World!"}

health_status = {"ready": False}

@app.get("/health")
async def health():
    if health_status["ready"]:
        return {"status": "healthy"}
    return {"status": "unhealthy"}, 503

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
