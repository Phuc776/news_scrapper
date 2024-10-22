import requests
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
PASSWORD_MYSQL = os.getenv('PASSWORD_MYSQL')

def init_connection_sql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port="1111",
            database="news_database",
            user="root",
            password=PASSWORD_MYSQL
        )
    except mysql.connector.Error as e:
        print(e)
        return None
    
    if connection.is_connected():
        print("Connected to MySQL database")
        return connection

    return None

con = init_connection_sql()

def bulk_insert_news(articles):
    """Bulk insert news data into the MySQL database."""
    connection = init_connection_sql()
    if connection is None:
        print("Failed to connect to the database.")
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
        print(f"{cursor.rowcount} records inserted successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def get_raw_data():
    """Get raw data from the Newscatcher API."""
    url = "https://api.newscatcherapi.com/v2/search"

    # You can customize the query parameter (e.g., "technology" or "sports")
    querystring = {"q":"technology", "lang":"en", "sort_by":"relevancy", "page":"1"}

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
    articles_date = get_raw_data()
    bulk_insert_news(articles_date)