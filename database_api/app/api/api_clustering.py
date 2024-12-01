from fastapi import APIRouter, Depends, HTTPException
from app.models import ClusteringResult
from datetime import datetime
from fastapi_sqlalchemy import db
from sqlalchemy import func
import asyncio

router = APIRouter()

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