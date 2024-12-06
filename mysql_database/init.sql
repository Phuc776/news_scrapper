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
    twitter_account VARCHAR(50),
    processed_text TEXT,
    sentiment_score FLOAT,
    sentiment_category INT, -- 1: very negative, 2: negative, 3: neutral, 4: positive, 5: very positive
    author_freq FLOAT,
    clean_url_freq FLOAT,
    country_freq FLOAT,
    twitter_account_freq FLOAT, 
    -- frequency encoded data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE clustering_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cluster_name VARCHAR(255),
    keywords TEXT,
    weights TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE correlation_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correlation_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sentiment_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(255),
    avg_sentiment_score FLOAT,
    article_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);