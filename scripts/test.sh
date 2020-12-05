#!/bin/bash

python database_session.py
&& PYTHONPATH=. alembic upgrade head
&& pytest --cov=. --cov-config=.coveragec -s --ignore=tests/test_data.py --ignore=tests/integration tests/