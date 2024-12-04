from sqlalchemy import Column, JSON
from app.models.model_base import BareBaseModel

class CorrelationData(BareBaseModel):
    __tablename__ = 'correlation_data'

    correlation_data = Column(JSON, nullable=False)