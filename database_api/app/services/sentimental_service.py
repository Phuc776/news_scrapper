from fastapi_sqlalchemy import db
from app.models import SentimentSummary, CorrelationData
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy import desc

class SentimentalService:

    @classmethod
    def get_all_sentimental_summaries(cls):
        return db.session.query(SentimentSummary).all()
    
    @classmethod
    def get_correlation_data(cls):
        return db.session.query(CorrelationData).order_by(desc(CorrelationData.created_at)).first()