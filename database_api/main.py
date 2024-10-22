import time
from flask import Flask, jsonify, request
import requests
import mysql.connector as connector
import logging as log
app = Flask(__name__)

logfile = 'dp_api.log'
log.basicConfig(filename=logfile, level=log.INFO)

process_timeout = {'timeout': 10,
                   'process': True}

mysql_service ='mysql_service'
# mysql_service ='localhost'
data_crawling = 'data_crawling'
# data_crawling = 'localhost'

def req(url):
    log.info(f"Requesting {url}")
    try:
        res = requests.get(url, timeout=process_timeout['timeout'])
        if res.status_code == 200:
            return res.json() if res is not None else req(url)
    except requests.Timeout:
        log.error("Request timed out")
    except requests.RequestException as e:
        log.error(f"Request failed: {e}")
    return {'error': 'error on request'} if process_timeout['process'] else req(url)

def connect_to_db():
    log.info('Connecting to database')
    db_config = { 
        'host': f'{mysql_service}',
        'port': '3307',
        'user': 'root',
        'password': 'rootpassword',
        'database': 'news_database'
    }
    for _ in range(20):
        try:
            conn = connector.connect(**db_config)
            log.info('Connected to database')
            return conn
        except connector.Error as e:
            log.error(e)
            log.info('Retrying...')
            time.sleep(5)