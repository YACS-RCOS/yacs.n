#!/bin/bash

DATA_FILE=fall-2022_data.json

if [ -f "$DATA_FILE" ]; then
    TARGET_FILE=fall-2022.csv DATA_FILE=fall-2022_data.json HAS_DATA=y DEBUG=n python3 modules/postProcess.py
else
    TARGET_FILE=fall-2022.csv DATA_FILE=fall-2022_data.json HAS_DATA=n DEBUG=n python3 modules/postProcess.py
fi
