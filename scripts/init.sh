#!/usr/bin/env bash
# NODE: run from project root (.)
export DB_PASS=dev_pass
docker-compose \
  -f docker-compose.yml up \
  --build
