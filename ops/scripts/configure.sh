#!/usr/bin/env bash

# <UDF name="branch" label="The BRANCH from which to deploy yacs">
# BRANCH=

apt update -y;
apt install docker -y;
apt install docker-compose -y;
git clone https://github.com/YACS-RCOS/yacs.n;
cd yacs.n;
git checkout $BRANCH;

# get info
GIT_STATUS_INFO=$(git status)

# build info file
INFO_FILE=_info/info.txt
mkdir -p _info;
echo "[build time]"   >> $INFO_FILE
date                  >> $INFO_FILE
echo "[git status]"   >> $INFO_FILE
echo $GIT_STATUS_INFO >> $INFO_FILE
echo "[build logs]"   >> $INFO_FILE

# start yacs
docker-compose up -d  >> $INFO_FILE

# start info server
cd _info/
apt install python3 -y;
python3 -m http.server 3000;
