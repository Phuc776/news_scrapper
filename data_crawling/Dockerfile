FROM python:3.9.16-slim-buster
COPY . /api
RUN pip install uvicorn fastapi
WORKDIR /api
CMD ["uvicorn", "data_crawling:app", "--host", "0.0.0.0", "--port", "8001"]