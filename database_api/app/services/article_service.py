from fastapi_sqlalchemy import db
from app.models import Article
from datetime import datetime
from sqlalchemy import and_

class ArticleService:

    @classmethod
    def get_all_articles(cls, topic: str = None, country: str = None, start_date: datetime = None, end_date: datetime = None):
        filters = []
        if topic:
            filters.append(Article.topic == topic)
        if country:
            filters.append(Article.country == country)
        if start_date:
            filters.append(Article.published_date >= start_date)
        if end_date:
            filters.append(Article.published_date <= end_date)
        
        return db.session.query(Article).filter(and_(*filters))
    
    @classmethod
    def get_all_topic(cls):
        return db.session.query(Article.topic).distinct().all()