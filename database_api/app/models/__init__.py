# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.model_base import Base  # noqa
from app.models.article import Article  # noqa
from app.models.clustering import ClusteringResult  # noqa