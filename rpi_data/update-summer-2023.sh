#!/bin/bash

DATA_FILE=summer-2023_data.json

if [ -f "$DATA_FILE" ]; then
    TARGET_FILE=summer-2023.csv DATA_FILE=summer-2023_data.json HAS_DATA=y DEBUG=y python3 modules/postProcess.py
else
    TARGET_FILE=summer-2023.csv DATA_FILE=summer-2023_data.json HAS_DATA=n DEBUG=y python3 modules/postProcess.py
fi
