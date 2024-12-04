from fastapi import APIRouter

from app.api import api_healthcheck, api_articles, api_clustering, api_sentimental

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["health-check"], prefix="/healthcheck")
router.include_router(api_articles.router, tags=["articles"], prefix="/articles")
router.include_router(api_clustering.router, tags=["keywords"], prefix="/clustering")
router.include_router(api_sentimental.router, tags=["sentimental"], prefix="/sentimental")