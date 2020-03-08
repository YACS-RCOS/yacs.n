#!/usr/bin/env bash
export SEMESTER="FALL 2020"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202009.htm DEST=p0.csv HEADERS=True python modules/rpi-parse.py
cat p* > fall-2020.csv
rm -rf p*.csv
