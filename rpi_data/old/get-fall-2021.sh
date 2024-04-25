#!/usr/bin/env bash
export SEMESTER="FALL 2021"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202109.htm DEST=p0.csv HEADERS=True python modules/rpi-parse.py
cat p* > fall-2021.csv
rm -rf p*.csv
