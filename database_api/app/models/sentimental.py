from sqlalchemy import Column, String, Integer, Float
from app.models.model_base import BareBaseModel

class SentimentSummary(BareBaseModel):
    __tablename__ = 'sentiment_summary'

    topic = Column(String(255), nullable=False)
    avg_sentiment_score = Column(Float, nullable=False)
    article_count = Column(Integer, nullable=False)