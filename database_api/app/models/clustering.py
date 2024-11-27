from sqlalchemy import Column, String
from app.models.model_base import BareBaseModel


class ClusteringResult(BareBaseModel):
    __tablename__ = 'clustering_results'

    cluster_name = Column(String(255)) 
    keywords = Column(String(255))
    weights = Column(String(255)) 