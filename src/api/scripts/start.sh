#!/usr/bin/env bash
python tables/database_session.py && 
PYTHONPATH=. alembic upgrade head &&
uvicorn app:app --host 0.0.0.0 --port 5000
