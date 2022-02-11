#!/usr/bin/env bash

spring() {
	local YEAR=${1}
	SOURCE_URL=https://sis.rpi.edu/reg/zfs${YEAR}01.htm
	if !(! curl -s --head  --request GET ${SOURCE_URL} | grep "404 Not Found" > /dev/null)
    then
			export SEMESTER="SPRING $YEAR"
			DEST=p0.csv HEADERS=True python3 modules/rpi-parse.py
			cat p* > spring-$YEAR.csv
			rm -rf p*.csv
}

summer() {
	local YEAR=${1}
	SOURCE_URL_A=https://sis.rpi.edu/reg/zfs${YEAR}05.htm
	SOURCE_URL_B=https://sis.rpi.edu/reg/zfs${YEAR}0502.htm
	SOURCE_URL_C=https://sis.rpi.edu/reg/zfs${YEAR}0503.htm
	if !((! curl -s --head  --request GET ${SOURCE_URL_A} | grep "404 Not Found" > /dev/null)
				&& (! curl -s --head  --request GET ${SOURCE_URL_B} | grep "404 Not Found" > /dev/null)
				&& (! curl -s --head  --request GET ${SOURCE_URL_C} | grep "404 Not Found" > /dev/null)
			)
    then
			export SEMESTER="SUMMER $YEAR"
			SOURCE_URL=$SOURCE_URL_A HEADERS=True python3 modules/rpi-parse.py
			SOURCE_URL=$SOURCE_URL_B HEADERS=False python ./modules/rpi-parse.py
			SOURCE_URL=$SOURCE_URL_C HEADERS=False python ./modules/rpi-parse.py
			cat p* > summer-$YEAR.csv
			rm -rf p*.csv
}

fall() {
	local YEAR=${1}
	SOURCE_URL=https://sis.rpi.edu/reg/zfs${YEAR}09.htm
	if !(! curl -s --head  --request GET ${SOURCE_URL} | grep "404 Not Found" > /dev/null)
    then
			export SEMESTER="SPRING $YEAR"
			DEST=p0.csv HEADERS=True python modules/rpi-parse.py
			cat p* > fall-$YEAR.csv
			rm -rf p*.csv
}


MONTH=$(date +%m)
YEAR=$(date +%y)
if [[$MONTH -ge 01 ]] && [[$MONTH -le 05]]
then
	spring(YEAR)
	summer(YEAR)

if [[$MONTH -ge 05 ]] && [[$MONTH -le 09]]
then
	summer(YEAR)
	fall(YEAR)

if [[$MONTH -ge 09 ]] || [[$MONTH -eq 01]]
then
	fall(YEAR)
	spring(YEAR)