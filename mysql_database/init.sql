CREATE DATABASE IF NOT EXISTS news_database;

USE news_database;

CREATE TABLE news_articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    published_date DATETIME,
    published_date_precision VARCHAR(50),
    link TEXT,
    clean_url VARCHAR(255),
    excerpt TEXT,
    summary TEXT,
    rights VARCHAR(255),
    rank_news INT,
    topic VARCHAR(50),
    country VARCHAR(10),
    language VARCHAR(10),
    authors TEXT,
    media TEXT,
    is_opinion BOOLEAN,
    twitter_account VARCHAR(50)
);
