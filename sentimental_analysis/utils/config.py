from dotenv import load_dotenv
import os

"""Load environment variables from .env file."""

load_dotenv()

API_KEY = os.getenv('API_KEY')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
DB_PASSWORD = os.getenv('DB_PASSWORD')