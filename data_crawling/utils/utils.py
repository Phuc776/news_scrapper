import mysql.connector
from dotenv import load_dotenv
from utils.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
from utils.logger import AppLog

load_dotenv()

def init_connection_sql():
    """Initialize a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except mysql.connector.Error as error:
        AppLog.error(f"Failed to connect to the database: {error}")
        return None
    
    if connection.is_connected():
        AppLog.info("Connection established to MySQL Database.")
        return connection

    return None