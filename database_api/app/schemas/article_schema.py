from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ArticleSchema(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published_date: Optional[datetime]
    published_date_precision: Optional[str]
    link: Optional[str]
    clean_url: Optional[str]
    excerpt: Optional[str]
    summary: Optional[str]
    rights: Optional[str]
    rank_news: Optional[int]
    topic: Optional[str]
    country: Optional[str]
    language: Optional[str]
    authors: Optional[str]
    media: Optional[str]
    is_opinion: Optional[bool]
    twitter_account: Optional[str]

    class Config:
        orm_mode = True