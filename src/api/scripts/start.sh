#!/usr/bin/env bash
echo "using $WORKERS workers to server api"
gunicorn --bind 0.0.0.0:5000 -w $WORKERS wsgi:app
