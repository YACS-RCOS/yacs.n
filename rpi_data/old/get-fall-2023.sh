#!/usr/bin/env bash
export SEMESTER="FALL 2023"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202309.htm DEST=p0.csv HEADERS=True python modules/rpi-parse.py
cat p* > fall-2023.csv
rm -rf p*.csv
