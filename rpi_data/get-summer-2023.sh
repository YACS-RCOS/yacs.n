#!/usr/bin/env bash
export SEMESTER="SUMMER 2023"
SOURCE_URL=https://sis.rpi.edu/reg/zs20230501.htm DEST=p0.csv HEADERS=True python ./modules/rpi-parse.py
SOURCE_URL=https://sis.rpi.edu/reg/zs20230502.htm DEST=p1.csv HEADERS=False python ./modules/rpi-parse.py
SOURCE_URL=https://sis.rpi.edu/reg/zs20230503.htm DEST=p2.csv HEADERS=False python ./modules/rpi-parse.py
cat p* > summer-2023.csv
rm -rf p*.csv
