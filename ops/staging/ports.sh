#!/bin/bash
# Lockfile
LOCKFD=233
LOCKFS=~/port.lock
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

# Minimum port to use
LOWERPORT=8100
# Largest port to use
UPPERPORT=9100

# Critical
lock || err $0 "cannot acquire a lock"
trap unlock EXIT
# Assign a random port from lower to upper
port=$(comm -23 <(seq "$LOWERPORT" "$UPPERPORT") \
                <(ss -Htan | awk '{print $4}' | cut -d':' -f2 | sort -u)\
            | shuf | head -n "1")

# Export the port number
echo $port
# Critical end
unlock
