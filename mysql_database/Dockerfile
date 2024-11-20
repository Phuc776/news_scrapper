# Use the official MySQL image from the Docker Hub
FROM mysql:latest

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=${DB_PASSWORD}
ENV MYSQL_DATABASE=news_database

# Copy the initialization SQL script to the Docker container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the MySQL port on 3307
EXPOSE 3307

# Change the MySQL configuration to listen on port 3307
CMD ["mysqld", "--port=3307"]