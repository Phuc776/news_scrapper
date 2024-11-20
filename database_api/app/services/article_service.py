from fastapi_sqlalchemy import db
from app.models import Article


class ArticleService:

    @classmethod
    def get_all_articles(cls):
        return db.session.query(Article)