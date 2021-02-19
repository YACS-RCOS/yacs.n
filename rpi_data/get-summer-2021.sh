#!/usr/bin/env bash
export SEMESTER="SUMMER 2021"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202105.htm DEST=p0.csv HEADERS=True python3 modules/rpi-parse.py
cat p* > summer-2021.csv
rm -rf p*.csv
