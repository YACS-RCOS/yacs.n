#!/bin/bash

DATA_FILE=spring-2023_data.json

if [ -f "$DATA_FILE" ]; then
    TARGET_FILE=spring-2023.csv DATA_FILE=spring-2023_data.json HAS_DATA=y DEBUG=n python3 modules/postProcess.py
else
    TARGET_FILE=spring-2023.csv DATA_FILE=spring-2023_data.json HAS_DATA=n DEBUG=n python3 modules/postProcess.py
fi
