from fastapi import APIRouter, Depends, HTTPException
from app.services import ArticleService
from app.schemas import ArticleSchema
from app.models import Article
from app.helpers.paging import Page, PaginationParams, paginate

router = APIRouter()

@router.get("", response_model=Page[ArticleSchema])
def get_all_articles(params: PaginationParams = Depends()):
    try:
        query = ArticleService.get_all_articles()
        articles = paginate(model=Article, query=query, params=params)
        return articles
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))