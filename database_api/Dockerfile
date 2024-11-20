FROM python:3.9.16-slim-buster

ENV SQL_DATABASE_URL=${SQL_DATABASE_URL}
ENV PROJECT_NAME=${PROJECT_NAME}

COPY . /api

RUN pip install -r /api/requirements.txt

WORKDIR /api

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
