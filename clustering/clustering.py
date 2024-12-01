import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from utils.utils import init_connection_sql
from utils.logger import AppLog
from datetime import datetime
import nltk
nltk.download('punkt')
nltk.download('stopwords')

class TextClustering:
    def __init__(self, data_json):
        """
        Khởi tạo lớp clustering với dữ liệu JSON.
        """
        self.data_json = data_json

    @staticmethod
    def clean_data(data_json):
        """
        Làm sạch dữ liệu JSON: loại bỏ các giá trị null ở cột 'title', 'summary', 'author'.
        """
        data = pd.DataFrame(data_json)
        data.dropna(subset=['title', 'summary', 'author'], inplace=True)
        return data

    @staticmethod
    def preprocess_text(text):
        """
        Xử lý văn bản bằng cách loại bỏ ký tự đặc biệt, chuyển chữ thường, token hóa,
        và loại bỏ stopwords.
        """
        stop_words = set(stopwords.words('english'))
        text = re.sub(r'\W+', ' ', text.lower())
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(filtered_tokens)

    def perform_clustering(self):
        """
        Thực hiện clustering trên dữ liệu.
        """
        # Làm sạch và xử lý dữ liệu
        data = self.clean_data(self.data_json)
        data['text'] = data['title'] + ' ' + data['summary'] + ' ' + data['author']
        data['processed_text'] = data['text'].apply(self.preprocess_text)
        data = data[data['processed_text'].str.strip() != '']

        if data.empty:
            raise ValueError("No valid documents to cluster after preprocessing.")

        # Vector hóa dữ liệu
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(data['processed_text'])
        n_samples = X.shape[0]

        if n_samples < 2:
            raise ValueError("Not enough samples to perform clustering.")

        # Tìm số cluster tối ưu
        best_n_clusters = 5
        best_score = -1

        for n_clusters in range(2, min(11, n_samples)):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, init='k-means++', max_iter=300, n_init=10)
            kmeans.fit(X)
            score = silhouette_score(X, kmeans.labels_)
            if score > best_score:
                best_score = score
                best_n_clusters = n_clusters

        # Gán cluster labels
        kmeans = KMeans(n_clusters=best_n_clusters, random_state=42, init='k-means++', max_iter=300, n_init=10)
        y_kmeans = kmeans.fit_predict(X)

        return vectorizer, X, y_kmeans, best_n_clusters

    def save_clustered_data(self):
        """
        Lưu kết quả clustering vào cơ sở dữ liệu MySQL.
        """
        AppLog.info(f"Saving clustering results to the database at {datetime.now()}")
        connection = init_connection_sql()
        if connection is None:
            AppLog.error("Error: Could not establish a MySQL connection.")
            return

        try:
            # Thực hiện clustering
            vectorizer, X, y_kmeans, best_n_clusters = self.perform_clustering()
            terms = vectorizer.get_feature_names_out()
            top_n = 20

            # Ghi kết quả clustering vào cơ sở dữ liệu
            for i in range(best_n_clusters):
                # Lấy các từ khóa quan trọng nhất
                cluster_data = X[y_kmeans == i].toarray()
                sum_terms = cluster_data.sum(axis=0)
                sorted_idx = sum_terms.argsort()[::-1]

                cluster_name = f"Cluster {i + 1}"
                keywords = ','.join([terms[idx] for idx in sorted_idx[:top_n]])
                weights = ','.join([str(sum_terms[idx]) for idx in sorted_idx[:top_n]])

                # Ghi vào cơ sở dữ liệu
                cursor = connection.cursor()
                insert_query = """
                    INSERT INTO clustering_results (cluster_name, keywords, weights, created_at, updated_at)
                    VALUES (%s, %s, %s, NOW(), NOW())
                """
                cursor.execute(insert_query, (cluster_name, keywords, weights))
                cursor.close()

            # Lưu thay đổi
            connection.commit()

        except Exception as e:
            AppLog.error(f"Error during clustering or saving data: {e}")
            connection.rollback()

        finally:
            connection.close()

        AppLog.info("Clustering results have been saved to the database.")


# Hàm thực thi clustering
def run_clustering():
    """
    Lấy dữ liệu từ cơ sở dữ liệu `news_articles`, thực hiện clustering và lưu kết quả.
    """
    connection = init_connection_sql()
    if connection is None:
        AppLog.error("Error: Could not establish a MySQL connection.")
        return

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT title, summary, author
            FROM news_articles
            WHERE title IS NOT NULL AND summary IS NOT NULL AND author IS NOT NULL
            LIMIT 1000;
        """
        cursor.execute(query)
        data_json = cursor.fetchall()
        cursor.close()

        if not data_json:
            AppLog.info("No data available for clustering.")
            return

        clustering = TextClustering(data_json)
        clustering.save_clustered_data()

    except Exception as e:
        AppLog.error(f"Error fetching data: {e}")

    finally:
        connection.close()


if __name__ == "__main__":
    run_clustering()
