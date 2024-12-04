from fastapi import APIRouter, Depends, HTTPException
from app.services import SentimentalService
from datetime import datetime

router = APIRouter()

@router.get("/summaries")
def get_all_sentimental_summaries():
    try:
        return SentimentalService.get_all_sentimental_summaries()
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))
    
@router.get("/correlation")
def get_correlation_data():
    try:
        return SentimentalService.get_correlation_data()
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=str(error))