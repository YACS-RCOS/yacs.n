#!/usr/bin/env bash

# first stop
docker-compose stop

# then remove old containers
docker-compose rm -f
