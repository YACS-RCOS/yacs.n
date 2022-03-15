#!/usr/bin/env bash

# <UDF name="branch" label="The BRANCH from which to deploy yacs">
# BRANCH=

apt update -y
apt install docker -y
apt install docker-compose -y
git clone https://github.com/YACS-RCOS/yacs.n
cd yacs.n
git checkout $BRANCH

# get info
GIT_STATUS_INFO=$(git status)

# build info file
INFO_FILE="/_info/info.txt"
mkdir -p /_info/

echo "[build time]"   >> $INFO_FILE
date                  >> $INFO_FILE
echo "[git status]"   >> $INFO_FILE
echo $GIT_STATUS_INFO >> $INFO_FILE
echo "[build logs]"   >> $INFO_FILE

# start info server in sub-shell
(
    cd /_info/
    apt install python3 -y
    python3 -m http.server 3000 &
    # start logging
)


# start yacs
bash scripts/start.sh >> $INFO_FILE

# seed pr/feature deploys with sample data
echo "[seeding data]" >> $INFO_FILE
function load_semester() {
    echo "$(date) [INFO] seeding: $1" >> $INFO_FILE
    curl \
        --location \
        --request POST \
        'http://localhost/api/bulkCourseUpload' \
        --form "file=@$1" \
        --form 'isPubliclyVisible=true' \
        --max-time 60 \
        -v
}

load_semester "rpi_data/summer-2020.csv"
load_semester "rpi_data/fall-2020.csv"
