#!/bin/bash

pytest --cov=. --cov-config=.coveragec -s --ignore=tests/test_data.py --ignore=tests/integration tests/