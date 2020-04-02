#!/usr/bin/env bash

# defaults
TAIL_LENGTH=10
PATH_ROOT=$(pwd)

# make directory for logs and create log files
mkdir -p logs
echo "" > $PATH_ROOT/logs/api.txt
echo "" > $PATH_ROOT/logs/web.txt
echo "Starting @ $(date)" > $PATH_ROOT/logs/dev.txt

# run flask
cd src/api/
flask run --reload >> $PATH_ROOT/logs/api.txt 2>&1 & # run in bg and port logs
FLASK_PID=($!)
echo "FLASK_PID: $FLASK_PID" >> $PATH_ROOT/logs/dev.txt
cd ../..

# run frontend
cd src/web/
npm run serve >> $PATH_ROOT/logs/web.txt 2>&1 &
WEB_PID=($!)
echo "WEB_PID: $WEB_PID" >> $PATH_ROOT/logs/dev.txt
cd ../..

# kill processes on ctrl-c
function cleanup() {
  echo "------------------------------------"
  echo "cleaning up..."
  echo "killing(FLASK_PID:$FLASK_PID)"
  kill $FLASK_PID
  echo "killing(WEB_PID:$WEB_PID)"
  kill $WEB_PID
}
trap cleanup EXIT

while [[ true ]]
do
  printf "\033c"
  echo "-----------------------------------"
  echo "dev runner logs"
  echo "-----------------------------------"
  tail -n $TAIL_LENGTH $PATH_ROOT/logs/dev.txt
  echo "-----------------------------------"
  echo "api logs: [last $TAIL_LENGTH lines]"
  echo "-----------------------------------"
  tail -n $TAIL_LENGTH $PATH_ROOT/logs/api.txt
  echo "-----------------------------------"
  echo "web logs: [last $TAIL_LENGTH lines]"
  echo "-----------------------------------"
  tail -n $TAIL_LENGTH $PATH_ROOT/logs/web.txt
  sleep 0.5
done
