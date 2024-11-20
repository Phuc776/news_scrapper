FROM python:3.9.16-slim-buster

ENV API_KEY=${API_KEY}
ENV DB_HOST=${DB_HOST}
ENV DB_USER=${DB_USER}
ENV DB_NAME=${DB_NAME}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_PORT=${DB_PORT}

COPY . /api

RUN pip install -r /api/requirements.txt

WORKDIR /api

CMD ["uvicorn", "crawl:app", "--host", "0.0.0.0", "--port", "8001"]
