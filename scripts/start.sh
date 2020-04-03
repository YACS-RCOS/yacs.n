#!/usr/bin/env bash
# NODE: run from project root (.)
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.production.yml \
  up \
  --force-recreate
