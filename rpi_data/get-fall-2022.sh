#!/usr/bin/env bash
export SEMESTER="FALL 2022"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202209.htm DEST=p0.csv HEADERS=True python3 modules/rpi-parse.py
cat p* > fall-2022.csv
rm -rf p*.csv