#!/usr/bin/env bash
# NODE: run from project root (.)
docker-compose \
  -f docker-compose.yml up \
  --build \
  --force-recreate
