FROM python:3.8-slim

ENV PYTHONPATH=/usr/src

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]