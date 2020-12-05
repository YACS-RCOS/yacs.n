#!/bin/bash

python src/api/database_session.py && 
PYTHONPATH=src/api alembic upgrade head && 
pytest --cov=. --cov-config=.coveragec -s --ignore=tests/test_data.py --ignore=tests/integration tests/