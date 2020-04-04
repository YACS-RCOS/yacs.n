#!/usr/bin/env bash
export SEMESTER="SPRING 2020"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202001.htm DEST=p0.csv HEADERS=True python modules/rpi-parse.py
cat p* > spring-2020.csv
rm -rf p*.csv
