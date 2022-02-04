#!/bin/bash
# Lockfile
LOCKFD=235
LOCKFS=~/nginx.lock
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
BKNGX_PORT=$1
NGINX_PORT=$2
SVHOSTNAME=$3
NGINX_DIR=/etc/nginx


