import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from utils.logger import AppLog
from datetime import datetime
from utils.utils import init_connection_sql

class SentimentalAnalysis:
    def __init__(self, data_json):
        """
        Initialize the SentimentalAnalysis class with data in JSON format.
        """
        self.data_json = data_json

    def analyze(self):
        """
        Analyze sentiment on the given data and categorize sentiment scores.
        """
        df = pd.DataFrame(self.data_json)
        if df.empty:
            raise ValueError("No valid documents to perform sentiment analysis.")
        
        analyzer = SentimentIntensityAnalyzer()
        df['combined_text'] = df['title'] + ' ' + df['summary'] + ' ' + df['author']
        df['sentiment_score'] = df['combined_text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])

        def sentiment_category(score):
            if score >= 0.6:
                return 5  # Very positive
            elif score >= 0.2:
                return 4  # Positive
            elif score > -0.2:
                return 3  # Neutral
            elif score > -0.6:
                return 2  # Negative
            else:
                return 1  # Very negative

        df['sentiment_category'] = df['sentiment_score'].apply(sentiment_category)
        
        # Assuming frequency encoding is already performed outside of this class
        return df

    def save_result(self):
        """
        Save the sentiment analysis results to the `news_articles` table in MySQL.
        """
        AppLog.info(f"Start saving sentiment analysis result to the database at {datetime.now()}.")
        connection = init_connection_sql()
        if connection is None:
            AppLog.error("Error: Could not establish a MySQL connection.")
            return
        
        try:
            cursor = connection.cursor()
            update_query = """
                UPDATE news_articles
                SET processed_text = %s, sentiment_score = %s, sentiment_category = %s,
                    author_freq = %s, clean_url_freq = %s, country_freq = %s, twitter_account_freq = %s,
                    updated_at = NOW()
                WHERE id = %s
            """

            data_to_update = [
                (
                    row['processed_text'], row['sentiment_score'], row['sentiment_category'],
                    row['author_freq'], row['clean_url_freq'], row['country_freq'], row['twitter_account_freq'],
                    row['id']
                )
                for _, row in self.analyze().iterrows()
            ]

            cursor.executemany(update_query, data_to_update)
            connection.commit()
            AppLog.info(f"{cursor.rowcount} records updated successfully at {datetime.now()}.")
        
        except Exception as e:
            AppLog.error(f"Failed to update data in MySQL table: {e}")
            connection.rollback()
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    pass  # This will be handled in the main.py file.
