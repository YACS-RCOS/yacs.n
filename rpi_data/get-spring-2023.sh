#!/bin/zsh
export SEMESTER="SPRING 2023"
SOURCE_URL=https://sis.rpi.edu/reg/zfs202301.htm DEST=p0.csv HEADERS=True python3 modules/rpi-parse.py
cat p* > spring-2023.csv
rm -rf p*.csv

./update-spring-2023.sh