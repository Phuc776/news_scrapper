# NewScrapper API

NewScrapper API is a microservice-based Python project designed for web scraping, storing, and providing APIs to access news articles. It consists of three main modules: mysql-service, data-crawling (data ingestion), and db-api (API provider). The project is built to be scalable and modular, allowing each service to operate independently.

Following Newscatcher API for more. [https://www.newscatcherapi.com/](https://www.newscatcherapi.com/)
## Modules

### 1. mysql-service
This service is responsible for handling all database operations. It sets up and manages the MySQL database, where the scraped data is stored.

- **Technologies Used:** Python, MySQL
- **Main Functionality:**
  - Database schema management
  - CRUD operations for managing news articles
  - Database connection and pooling

### 2. data-crawling (Data Ingestion)
The data-crawling module fetches data from the [Newscatcher API](https://www.newscatcherapi.com/). It collects news articles from various sources, cleans the data, and stores it in the MySQL database.

- **Technologies Used:** Python, Newscatcher API
- **Main Functionality:**
  - Fetch news articles from the Newscatcher API
  - Extract relevant data (e.g., titles, content, publication dates)
  - Store the data in the MySQL database through `mysql-service`

### 3. db-api (API Provider)
The db-api module provides a set of RESTful APIs that allow external services to access the scraped news data. This service interacts with the MySQL database and provides APIs for fetching news articles, searching, and filtering.

- **Technologies Used:** Python, Flask
- **Main Functionality:**
  - Provide RESTful APIs to access news data
  - Search and filter news articles by title, date, or source
  - Handle pagination and sorting
