#!/usr/bin/env bash

# first stop
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.production.yml \
  stop

# then remove old containers
docker-compose \
  -f docker-compose.yml \
  -f docker-compose.production.yml \
  rm -f

