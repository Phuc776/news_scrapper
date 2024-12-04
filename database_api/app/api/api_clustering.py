from fastapi import APIRouter, Depends, HTTPException
from app.models import ClusteringResult
from datetime import datetime
from fastapi_sqlalchemy import db
from sqlalchemy import func
from datetime import date
from typing import Optional
router = APIRouter()

@router.get("/keywords")
def get_all_keywords(created_at: Optional[date] = None):
    if not created_at:
        created_at = datetime.now().date()

    try:
        query = db.session.query(ClusteringResult).filter(func.date(ClusteringResult.created_at) == created_at)
        keyword_clusterings = query.all()
        return keyword_clusterings
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))

@router.get("/distinct-dates")
def get_distinct_dates():
    try:
        query = db.session.query(func.date(ClusteringResult.created_at).label('created_date')).distinct()
        distinct_dates = query.all()
        return [record.created_date for record in distinct_dates]
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))