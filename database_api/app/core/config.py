import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'FASTAPI BASE')
    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    API_PREFIX: str = ''
    BACKEND_CORS_ORIGINS: list = ['*']
    DATABASE_URL: str = os.getenv('SQL_DATABASE_URL', '')
    LOGGING_CONFIG_FILE: str = os.path.join(BASE_DIR, 'logging.ini')

settings = Settings()
