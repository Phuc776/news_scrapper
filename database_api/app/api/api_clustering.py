from fastapi import APIRouter, Depends, HTTPException
from app.services import ArticleService
from app.services.clustering_service import ClusteringService
from app.models import Article, ClusteringResult
from datetime import datetime
from fastapi_sqlalchemy import db
from sqlalchemy import func
import asyncio

router = APIRouter()

async def periodic_clustering():
    """Periodically cluster articles every 24 hours."""
    while True:
        try:
            with db():
                query = ArticleService.get_all_articles()
                today = datetime.today().date()
                query = query.filter(func.date(Article.created_at) == today)

                articles = query.all()
                articles_dict = [article.__dict__ for article in articles]

                if articles_dict:
                    clustering_service = ClusteringService(data_json=articles_dict)
                    clustering_service.save_clustered_data()
                    print("Clustering data saved successfully.")
                else:
                    print("No articles found for clustering.")
        except Exception as e:
            print(f"Error during clustering: {e}")

        await asyncio.sleep(86400)  # 24 hours

@router.post("/save-data")
def save_keyword_clusterings():
    try:
        query = ArticleService.get_all_articles()
        today = datetime.today().date()
        print(today)
        query = query.filter(func.date(Article.created_at) == today)

        articles_dict = [article.__dict__ for article in query.all()]
        if len(articles_dict) == 0:
            return {
                "message": "No articles found for today",
                "success": False
            }
        
        ClusteringService(data_json=articles_dict).save_clustered_data()
        return {
            "message": "Data saved successfully",
            "success": True
        }
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))

@router.get("/keywords")
def get_all_keywords(created_at: datetime = Depends(lambda: datetime.now())):
    try:
        query = db.session.query(ClusteringResult)
        query = query.filter(func.date(ClusteringResult.created_at) == created_at.date())
        keyword_clusterings = query.all()
        return keyword_clusterings
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))