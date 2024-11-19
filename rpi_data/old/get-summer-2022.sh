#!/usr/bin/env bash
export SEMESTER="SUMMER 2022"
SOURCE_URL=https://sis.rpi.edu/reg/zs202205.htm DEST=p0.csv HEADERS=True python ./modules/rpi-parse.py
SOURCE_URL=https://sis.rpi.edu/reg/zs20220502.htm DEST=p1.csv HEADERS=False python ./modules/rpi-parse.py
SOURCE_URL=https://sis.rpi.edu/reg/zs20220503.htm DEST=p2.csv HEADERS=False python ./modules/rpi-parse.py
cat p* > summer-2022.csv
rm -rf p*.csv
