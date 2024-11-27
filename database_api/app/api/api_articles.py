from fastapi import APIRouter, Depends, HTTPException
from app.services import ArticleService
from app.schemas import ArticleSchema
from app.models import Article
from app.helpers.paging import Page, PaginationParams, paginate
from datetime import datetime

router = APIRouter()

@router.get("", response_model=Page[ArticleSchema])
def get_all_articles(
    params: PaginationParams = Depends(),
    topic: str = None,
    country: str = None,
    start_date: datetime = None,
    end_date: datetime = None
):
    try:
        query = ArticleService.get_all_articles(
            topic=topic,
            country=country,
            start_date=start_date,
            end_date=end_date
        )
        articles = paginate(model=Article, query=query, params=params)

        return articles
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
