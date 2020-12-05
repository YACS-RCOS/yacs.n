#!/usr/bin/env bash
python database_session.py && 
PYTHONPATH=. alembic upgrade head &&
gunicorn --bind 0.0.0.0:5000 -w $WORKERS wsgi:app
