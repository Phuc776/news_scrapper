import requests
import mysql.connector
from utils.logger import AppLog
from utils.config import API_KEY
from utils.utils import init_connection_sql
import datetime

def insert_to_db(articles):
    """Bulk insert news data into the MySQL database."""
    AppLog.info(f"Start inserting {len(articles)} records to the database at {datetime.datetime.now()}.")
    connection = init_connection_sql()
    if connection is None:
        AppLog.error("Error: Could not establish a MySQL connection.")
        return

    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO news_articles (
                title, author, published_date, published_date_precision, link, clean_url, excerpt, summary, rights, `rank_news`, topic, country, language, authors, media, is_opinion, twitter_account
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data_to_insert = [
            (
                article.get('title'),
                article.get('author'),
                article.get('published_date'),
                article.get('published_date_precision'),
                article.get('link'),
                article.get('clean_url'),
                article.get('excerpt'),
                article.get('summary'),
                article.get('rights'),
                article.get('rank'),
                article.get('topic'),
                article.get('country'),
                article.get('language'),
                article.get('authors'),
                article.get('media'),
                article.get('is_opinion'),
                article.get('twitter_account')
            )
            for article in articles
        ]

        cursor.executemany(insert_query, data_to_insert)
        connection.commit()
        AppLog.info(f"{cursor.rowcount} records inserted successfully at {datetime.datetime.now()}.")

    except mysql.connector.Error as error:
        AppLog.error(f"Failed to insert data into MySQL table: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_raw_data():
    """Get raw data from the Newscatcher API."""
    url = "https://api.newscatcherapi.com/v2/search"

    # You can customize the query parameter (e.g., "technology" or "sports")
    querystring = {"q":"*", "lang":"en", "sort_by":"date", "page_size": 100, "page": 1, "from_rank": 1, "to_rank": 10000}

    headers = {
        'x-api-key': API_KEY
    }

    # Make the request to the Newscatcher API
    response = requests.get(url, headers=headers, params=querystring)

    # Check if the response is successful
    if response.status_code == 200:
        # Save the results to a file
        return response.json().get("articles", [])

if __name__ == "__main__":
    while True:
        articles_data = get_raw_data()
        insert_to_db(articles_data)