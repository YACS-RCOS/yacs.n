#!/usr/bin/env bash

docker-compose \
  -f docker-compose.yml \
  -f docker-compose.development.yml \
  run --rm -e PYTHONPATH=/usr/src\
  yacs_api \
  alembic revision --autogenerate -m "$1"
