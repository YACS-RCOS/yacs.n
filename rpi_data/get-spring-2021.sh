#!/usr/bin/env bash
export SEMESTER="SPRING 2021"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202101.htm DEST=p0.csv HEADERS=True python modules/rpi-parse.py
cat p* > spring-2021.csv
rm -rf p*.csv
