#!/usr/bin/env bash
export SEMESTER="SUMMER 2020"
SOURCE_URL=https://sis.rpi.edu/reg/zs20200501.htm DEST=p0.csv HEADERS=True python ./modules/rpi-parse.py
SOURCE_URL=https://sis.rpi.edu/reg/zs20200502.htm DEST=p1.csv HEADERS=False python ./modules/rpi-parse.py
SOURCE_URL=https://sis.rpi.edu/reg/zs20200503.htm DEST=p2.csv HEADERS=False python ./modules/rpi-parse.py
cat p* > summer-2020.csv
rm -rf p*.csv
