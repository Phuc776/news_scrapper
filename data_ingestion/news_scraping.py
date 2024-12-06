import requests
import mysql.connector
from utils.logger import AppLog
from utils.config import API_KEY
from utils.utils import init_connection_sql
from datetime import datetime, timedelta
import joblib
import re
import os

model_path = os.path.join(os.path.dirname(__file__), 'Models', 'topic_classifier.pkl')
vectorizer_path = os.path.join(os.path.dirname(__file__), 'Models', 'tfidf_vectorizer.pkl')

# Load the models
classifier = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

valid_labels = {'sport', 'tech', 'world', 'finance', 'politics', 'business',
                'economics', 'entertainment', 'beauty', 'travel', 'music',
                'food', 'science', 'gaming', 'energy'}


# Text preprocessing function
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters
    return text

# Function to label topics for articles
def label_topics(articles):
    for article in articles:
        combined_text = preprocess_text(article.get('title', '') + ' ' + article.get('summary', ''))
        tfidf_vector = vectorizer.transform([combined_text])  # Transform text using the loaded vectorizer
        predicted_topic = classifier.predict(tfidf_vector)[0]  # Predict the topic
        
        # Update the topic only if it's not in the valid set
        if article.get('topic') not in valid_labels:
            article['topic'] = predicted_topic
    return articles

def insert_to_db(articles):
    """Bulk insert news data into the MySQL database."""
    AppLog.info(f"Start inserting {len(articles)} records to the database at {datetime.now()}.")

    # Label topics before inserting
    articles = label_topics(articles)

    connection = init_connection_sql()
    if connection is None:
        AppLog.error("Error: Could not establish a MySQL connection.")
        return

    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO news_articles (
                title, author, published_date, published_date_precision, link, clean_url, excerpt, summary, rights, `rank_news`, topic, country, language, authors, media, is_opinion, twitter_account, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        now = datetime.now()
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
                article.get('twitter_account'),
                now,
                now
            )
            for article in articles
        ]

        cursor.executemany(insert_query, data_to_insert)
        connection.commit()
        AppLog.info(f"{cursor.rowcount} records inserted successfully at {datetime.now()}.")

    except mysql.connector.Error as error:
        AppLog.error(f"Failed to insert data into MySQL table: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_raw_data(page=1):
    """Get raw data from the Newscatcher API."""
    url = "https://api.newscatcherapi.com/v2/search"

    # You can customize the query parameter (e.g., "technology" or "sports")
    querystring = {"q":"*", "lang":"en", "sort_by":"date", "page_size": 100, "page": page, "from_rank": 1, "to_rank": 10000}

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
    for i in range(20):
        try:
            articles_data = get_raw_data(page=i+1)  # Assuming get_raw_data is an async function
            insert_to_db(articles_data)  # Assuming insert_to_db is an async function
            AppLog.info(f"Successfully inserted batch {i+1} of articles.")
        except Exception as e:
            AppLog.error(f"Error occurred while processing batch {i+1}: {e}")
