from fastapi import FastAPI
app = FastAPI()
from news_scraping import get_raw_data, insert_to_db

@app.get("/crawl")
def crawl_data():
    """Crawl data from the Newscatcher API and insert it into the database."""
    while True:
        articles_data = get_raw_data()
        insert_to_db(articles_data)   