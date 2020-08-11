#!/bin/bash

bash src/data/build.sh

pytest --cov=. --cov-config=.coveragec -s --ignore=tests/test_data.py tests/