#!/bin/bash
# Lockfile
LOCKFD=234
LOCKFS=~/master.lock
# Open fd
eval "exec $LOCKFD>\"$LOCKFS\"" || { echo >&2 "$0: fd open failed"; exit 1; }
unlock() {
    flock -u $LOCKFD
    rm -f $LOCKFS
}
lock() {
    flock -xn $LOCKFD
}
err() {
    echo >&2 "$1: $2"
    exit 1
}
CUWD=$(pwd)
BKNGX_PORT=8082
NGINX_PORT=8081
SVHOSTNAME=yacs.duckdns.org

lock || err $0 "cannot acquire a lock"
# Unlock before exit
trap unlock EXIT

# Make sure the script runs in correct location
cd $CUWD

# Create staging folder, and delete existed master folder
echo "$0: creating directories"
mkdir ~/yacs-staging
rm -rf ~/yacs-staging/master
cd ~/yacs-staging || err $0 "cannot change directory"

# Clone the master and change directory
echo "$0: cloning master"
git clone https://github.com/YACS-RCOS/yacs.n master || err $0 "cannot clone repository"
cd master

# Configure the staging configuration
echo "$0: configuring staging configurations"
sed -i "s/65500945/$BKNGX_PORT/g" "docker-compose.staging.yml" || err $0 "replacing staging HTTP_PORT failed"
sed -i "s/69256173/$SVHOSTNAME/g" "docker-compose.staging.yml" || err $0 "replacing staging SERVER_NAME failed"

# Stop existed master docker
echo "$0: building dockers"
docker-compose -p master stop
# Remove master API and web
docker-compose -p master -f docker-compose.yml -f docker-compose.staging.yml rm -f yacs_api yacs_web
# Build master API and web, on error do exit
docker-compose -p master -f docker-compose.yml -f docker-compose.staging.yml build yacs_api yacs_web || err $0 "docker build master failed"
# Start the dockers
docker-compose -p master -f docker-compose.yml -f docker-compose.staging.yml up -d || err $0 "docker up master failed"
cd $CUWD

echo "$0: update nginx configurations"
./nginx.sh $BKNGX_PORT $NGINX_PORT $SVHOSTNAME || err $0 "nginx update failed"

unlock
cd $CUWD
