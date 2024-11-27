from app.utils.other_utils import clean_data, preprocess_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from fastapi_sqlalchemy import db
from app.models.clustering import ClusteringResult

class ClusteringService:
    def __init__(self, data_json):
        self.data_json = data_json

    def perform_clustering(self):
        data = clean_data(data_json=self.data_json)
        data['text'] = data['title'] + ' ' + data['summary'] + ' ' + data['author']
        data['processed_text'] = data['text'].apply(preprocess_text)  
        data = data[data['processed_text'].str.strip() != '']

        if data.empty:
            raise ValueError("No valid documents to cluster after preprocessing.")
        
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(data['processed_text'])    
        n_samples = X.shape[0]
        print(f"Number of samples: {n_samples}")
        if n_samples < 2:
            raise ValueError("Not enough samples to perform clustering.")
        
        best_n_clusters = 5  # Default
        best_score = -1 

        for n_clusters in range(2, min(11, n_samples)):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, init='k-means++', max_iter=300, n_init=10)
            kmeans.fit(X)
            score = silhouette_score(X, kmeans.labels_)
            if score > best_score:
                best_score = score
                best_n_clusters = n_clusters

        print(f"Best number of clusters: {best_n_clusters}")
        y_kmeans = kmeans.fit_predict(X)

        return vectorizer, X, y_kmeans , best_n_clusters
    
    def save_clustered_data(self):
        vectorizer, X, y_kmeans, best_n_clusters = self.perform_clustering()
        terms = vectorizer.get_feature_names_out()
        top_n = 20

        for i in range(best_n_clusters):
            cluster_terms = X[y_kmeans == i].toarray()
            sum_terms = cluster_terms.sum(axis=0)
            sorted_idx = sum_terms.argsort()[::-1]

            cluster_name = f"Cluster {i + 1}"
            keywords = ','.join([terms[idx] for idx in sorted_idx[:top_n]])
            weights = ','.join([str(sum_terms[idx]) for idx in sorted_idx[:top_n]])

            # Tạo đối tượng ClusteringResult
            clustering_result = ClusteringResult(
                cluster_name=cluster_name,
                keywords=keywords,
                weights=weights
            )

            # Thêm đối tượng vào session
            db.session.add(clustering_result)

        # Commit các thay đổi vào cơ sở dữ liệu
        db.session.commit()
        print("Clustering results have been saved to the database.")

