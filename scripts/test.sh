#!/bin/bash

bash src/data/build.sh

pytest --cov=. --cov-config=.coveragec -s tests/