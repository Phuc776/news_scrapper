from app.models.model_base import BareBaseModel
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, TIMESTAMP

MAX_LENGTH_MODEL_FIELD = 255

class Article(BareBaseModel):
    __tablename__ = 'news_articles'

    title = Column(Text)
    author = Column(String(MAX_LENGTH_MODEL_FIELD))
    published_date = Column(DateTime)
    published_date_precision = Column(String(MAX_LENGTH_MODEL_FIELD))
    link = Column(Text)
    clean_url = Column(String(MAX_LENGTH_MODEL_FIELD))
    excerpt = Column(Text)
    summary = Column(Text)
    rights = Column(String(MAX_LENGTH_MODEL_FIELD))
    rank_news = Column(Integer)
    topic = Column(String(MAX_LENGTH_MODEL_FIELD))
    country = Column(String(MAX_LENGTH_MODEL_FIELD))
    language = Column(String(MAX_LENGTH_MODEL_FIELD))
    authors = Column(Text)
    media = Column(Text)
    is_opinion = Column(Boolean)
    twitter_account = Column(String(MAX_LENGTH_MODEL_FIELD))