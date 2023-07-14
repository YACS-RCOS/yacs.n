FROM python:3.8-slim

RUN groupadd -r celery && useradd -r -g celery celery
ENV PYTHONPATH=/usr/src

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

USER celery


CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=debug", "--settings=celeryconfig"]