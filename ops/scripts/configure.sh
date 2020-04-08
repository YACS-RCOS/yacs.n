#!/usr/bin/env bash

# <UDF name="branch" label="The branch from which to deploy yacs">
# BRANCH=

apt update -y;
apt install docker -y;
apt install docker-compose -y;
git clone https://github.com/YACS-RCOS/yacs.n;
cd yacs.n;
git checkout $BRANCH
docker-compose up -d;
