#!/usr/bin/env bash
# NOTE: the second -f *.development.yml will override config from default docker-compose.yml
docker-compose -f docker-compose.yml -f docker-compose.development.yml build
# Clear database and web volumes
docker volume rm yacsn_postgres_data yacsn_web_node_modules
