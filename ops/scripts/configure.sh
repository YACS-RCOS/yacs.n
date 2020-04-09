#!/usr/bin/env bash

# <UDF name="commit_sha" label="The COMMIT_SHA from which to deploy yacs">
# COMMIT=

apt update -y;
apt install docker -y;
apt install docker-compose -y;
git clone https://github.com/YACS-RCOS/yacs.n;
cd yacs.n;
git checkout $COMMIT_SHA
docker-compose up -d;

# get info
GIT_STATUS_INFO=$(git status)

# show info at host:5000/info.txt
INFO_FILE=_info/info.txt
mkdir -p _info;

echo "[build time]"   >> $INFO_FILE
date                  >> $INFO_FILE
echo "[git status]"   >> $INFO_FILE
echo $GIT_STATUS_INFO >> $INFO_FILE

cd _info/

apt install python3 -y;
python3 -m http.server 3000;
