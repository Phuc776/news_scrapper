import requests
import mysql.connector
from nltk.stem import WordNetLemmatizer
import nltk
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from utils.logger import AppLog
from utils.config import API_KEY
from utils.utils import init_connection_sql
from datetime import datetime

def insert_to_db(articles):
    """Bulk insert news data into the MySQL database."""
    AppLog.info(f"Start inserting {len(articles)} records to the database at {datetime.now()}.")
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


def preprocess_text(text):
    """Preprocess the text data by removing special characters, stopwords, and lemmatizing the words."""
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-z\s]', '', text)  # Remove special characters
    words = nltk.word_tokenize(text)  # Tokenize
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

valid_labels = {'sport', 'tech', 'world', 'finance', 'politics', 'business',
                'economics', 'entertainment', 'beauty', 'travel', 'music',
                'food', 'science', 'gaming', 'energy'}
vectorizer = TfidfVectorizer(max_features=5000)
classifier = MultinomialNB()

def train_classifier(article_data):
    """Train a classifier to predict the topic of the article."""
    valid_articles = [article for article in article_data if article.get('topic') in valid_labels]
    if not valid_articles:
        return
    
    combined_texts = [preprocess_text(article.get('title', '') + ' ' + article.get('summary', '')) for article in valid_articles]
    topics = [article.get('topic') for article in valid_articles]
    
    X_train = vectorizer.fit_transform(combined_texts)
    classifier.fit(X_train, topics)
    AppLog.info("Classifier trained successfully with valid labeled data.")


def label_topic(articles):
    """Label the topic of each article based on the content."""
    for article in articles:
        title = article.get('title', '')
        summary = article.get('summary', '')
        combined_text = title + ' ' + summary
        cleaned_text = preprocess_text(combined_text)
        
        article['combined_text_processed'] = cleaned_text

        if article.get('topic') not in valid_labels:
            X_missing = vectorizer.transform([combined_text])
            predicted_topic = classifier.predict(X_missing)[0]
            article['topic'] = predicted_topic

if __name__ == "__main__":
    while True:
        for i in range(10):
            articles_data = get_raw_data()
            train_classifier(articles_data)
            label_topic(articles_data)
            insert_to_db(articles_data)