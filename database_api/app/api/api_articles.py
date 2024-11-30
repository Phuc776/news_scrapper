from fastapi import APIRouter, Depends, HTTPException
from app.services import ArticleService
from app.schemas import ArticleSchema
from app.models import Article
from app.helpers.paging import Page, PaginationParams, paginate
from datetime import datetime

router = APIRouter()

@router.get("/news-topics")
def get_count_articles_by_topic(
    start_date: datetime = None,
    end_date: datetime = None
):
    try:
        raw_topics = ArticleService.get_all_topic()
        topics = [t[0] for t in raw_topics]
        
        topics_with_count = []
        for topic in topics:
            count = ArticleService.get_all_articles(topic=topic, start_date=start_date, end_date=end_date).count()
            topics_with_count.append({"name": topic, "value": count})
        
        return topics_with_count
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))
    
@router.get("/news-countries")
def get_count_articles_by_topic(
    topic: str = None,
    start_date: datetime = None,
    end_date: datetime = None
):
    try:
        raw_countries = ArticleService.get_all_country()
        countries = [t[0] for t in raw_countries]
        
        coutry_with_count = []
        for country in countries:
            count = ArticleService.get_all_articles(country=country, topic=topic, start_date=start_date, end_date=end_date).count()
            coutry_with_count.append({"name": country, "value": count})
        
        return coutry_with_count
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))
    
@router.get("/topics")
def get_all_topic():
    raw_topics =  ArticleService.get_all_topic()
    topics = [t[0] for t in raw_topics]
    return {
        "topics": topics
    }
