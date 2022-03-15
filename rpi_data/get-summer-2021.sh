#!/usr/bin/env bash
export SEMESTER="SUMMER 2021"
SOURCE_URL=https://sis.rpi.edu/reg/zs202105.htm DEST=p0.csv HEADERS=True python ./modules/rpi-parse.py
SOURCE_URL=https://sis.rpi.edu/reg/zs20210502.htm DEST=p1.csv HEADERS=False python ./modules/rpi-parse.py
SOURCE_URL=https://sis.rpi.edu/reg/zs20210503.htm DEST=p2.csv HEADERS=False python ./modules/rpi-parse.py
cat p* > summer-2021.csv
rm -rf p*.csv
