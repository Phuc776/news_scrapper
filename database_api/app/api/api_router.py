from fastapi import APIRouter

from app.api import api_healthcheck, api_articles

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["health-check"], prefix="/healthcheck")
router.include_router(api_articles.router, tags=["articles"], prefix="/articles")