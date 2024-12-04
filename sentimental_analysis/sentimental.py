import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from utils.logger import AppLog
from datetime import datetime
from utils.utils import init_connection_sql
import json

class SentimentalAnalysis:
    def __init__(self, data_json):
        """
        Initialize the SentimentalAnalysis class with data in JSON format.
        """
        self.data_json = data_json

    def preprocess_and_analyze(self):
        """
        Perform sentiment analysis and frequency encoding on the data.
        """
        df = pd.DataFrame(self.data_json)
        if df.empty:
            raise ValueError("No valid documents to perform sentiment analysis.")
        
        df['author'] = df['author'].fillna('Unknown')
        df['author'] = df['author'].replace('', 'Unknown')
        df['clean_url'] = df['clean_url'].fillna('Unknown')
        df['country'] = df['country'].fillna('Unknown')
        df['twitter_account'] = df['twitter_account'].fillna('Unknown')

        df['author_freq'] = df['author'].map(df['author'].value_counts())
        df['clean_url_freq'] = df['clean_url'].map(df['clean_url'].value_counts())
        df['country_freq'] = df['country'].map(df['country'].value_counts())
        df['twitter_account_freq'] = df['twitter_account'].map(df['twitter_account'].value_counts())

        # Sentiment analysis
        analyzer = SentimentIntensityAnalyzer()
        df['combined_text'] = df['title'] + ' ' + df['summary']
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
        return df

    def save_result(self, processed_data):
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
                    row['combined_text'], row['sentiment_score'], row['sentiment_category'],
                    row['author_freq'], row['clean_url_freq'], row['country_freq'], row['twitter_account_freq'],
                    row['id']
                )
                for _, row in processed_data.iterrows()
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

    def calculate_and_save_correlation(self):
        """
        Calculate correlation for numeric columns and save the result as JSON.
        """
        connection = init_connection_sql()
        if connection is None:
            AppLog.error("Error: Could not establish a MySQL connection.")
            return

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT rank_news, sentiment_score, sentiment_category, author_freq, clean_url_freq, country_freq, twitter_account_freq FROM news_articles")
            data = cursor.fetchall()

            if not data:
                AppLog.info("No data available for correlation calculation.")
                return

            # Create a DataFrame and compute correlation
            df = pd.DataFrame(data)
            correlation_matrix = df.corr()

            # Convert correlation matrix to a nested JSON format
            correlation_dict = correlation_matrix.to_dict()
            correlation_json = json.dumps({"correlation_matrix": correlation_dict}, indent=4)

            # Save to the `correlation_data` table
            insert_query = "INSERT INTO correlation_data (correlation_data) VALUES (%s)"
            cursor.execute(insert_query, (correlation_json,))
            connection.commit()

            AppLog.info("Correlation data saved successfully.")
        
        except Exception as e:
            AppLog.error(f"Failed to calculate or save correlation data: {e}")
            connection.rollback()
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    def save_summary_result(self, processed_data):
        """
        Group data by topic and save average sentiment score and article count.
        """
        AppLog.info("Start saving sentiment summary to the database.")
        connection = init_connection_sql()
        if connection is None:
            AppLog.error("Error: Could not establish a MySQL connection.")
            return
        
        try:
            # Group by topic to calculate mean sentiment score and count
            sentiment_summary = processed_data.groupby('topic')['sentiment_category'].agg(['mean', 'count']).reset_index()
            
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO sentiment_summary (topic, avg_sentiment_score, article_count)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                avg_sentiment_score = VALUES(avg_sentiment_score),
                article_count = VALUES(article_count),
                updated_at = NOW()
            """
            
            data_to_insert = [
                (row['topic'], row['mean'], row['count'])
                for _, row in sentiment_summary.iterrows()
            ]

            cursor.executemany(insert_query, data_to_insert)
            connection.commit()
            AppLog.info(f"{cursor.rowcount} sentiment summary records saved successfully.")
        
        except Exception as e:
            AppLog.error(f"Failed to save sentiment summary data: {e}")
            connection.rollback()
        
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def run_sentiment_analysis():
    """Retrieve data from the database, process it, and save the sentiment analysis results"""
    connection = init_connection_sql()
    if connection is None:
        AppLog.error("Error: Could not establish a MySQL connection.")
        return
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM news_articles WHERE sentiment_score IS NULL")
        data = cursor.fetchall()

        if not data:
            AppLog.info("No data available for sentiment analysis.")
            return

        analyzer = SentimentalAnalysis(data)
        processed_data = analyzer.preprocess_and_analyze()
        analyzer.save_result(processed_data)
        analyzer.calculate_and_save_correlation()

    except Exception as e:
        AppLog.error(f"Failed to run sentiment analysis: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    pass  
