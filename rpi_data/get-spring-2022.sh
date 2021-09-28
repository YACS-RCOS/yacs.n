#!/usr/bin/env bash
export SEMESTER="SPRING 2022"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202201.htm DEST=p0.csv HEADERS=True python modules/rpi-parse.py
cat p* > spring-2022.csv
rm -rf p*.csv