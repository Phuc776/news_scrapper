FROM python:3.9.16-slim-buster
COPY . /api
RUN pip install -r /api/requirements.txt
WORKDIR /api
CMD ["uvicorn", "crawl:app", "--host", "0.0.0.0", "--port", "8001"]