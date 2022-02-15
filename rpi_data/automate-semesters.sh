#!/usr/bin/env bash

spring() {
	local year=${1}
	source_url=https://sis.rpi.edu/reg/zfs${year}01.htm
	if !(! curl -s --head  --request GET ${source_url} | grep "404 Not Found" > /dev/null)
	then
			export SEMESTER="SPRING ${year}"
			DEST=p0.csv HEADERS=True python3 modules/rpi-parse.py
			cat p* > spring-${year}.csv
			rm -rf p*.csv
	fi
}

summer() {
	local year=${1}
	source_url_a=https://sis.rpi.edu/reg/zfs${year}05.htm
	source_url_b=https://sis.rpi.edu/reg/zfs${year}0502.htm
	source_url_c=https://sis.rpi.edu/reg/zfs${year}0503.htm
	if !([[ ! curl -s --head  --request GET ${source_url_a} | grep "404 Not Found" > /dev/null ]]
				&& [[ ! curl -s --head  --request GET ${source_url_b} | grep "404 Not Found" > /dev/null ]]
				&& [[ ! curl -s --head  --request GET ${source_url_c} | grep "404 Not Found" > /dev/null ]]
			)
  then
			export SEMESTER="SUMMER ${year}"
			SOURCE_URL=${source_url_a} HEADERS=True python3 modules/rpi-parse.py
			SOURCE_URL=${source_url_b} HEADERS=False python3 ./modules/rpi-parse.py
			SOURCE_URL=${source_url_c} HEADERS=False python3 ./modules/rpi-parse.py
			cat p* > summer-${year}.csv
			rm -rf p*.csv
	fi
}

fall() {
	local year=${1}
	source_url=https://sis.rpi.edu/reg/zfs${year}09.htm
	if !(! curl -s --head  --request GET ${source_url} | grep "404 Not Found" > /dev/null)
	then
			export SEMESTER="FALL ${year}"
			DEST=p0.csv HEADERS=True python3 modules/rpi-parse.py
			cat p* > fall-${year}.csv
			rm -rf p*.csv
	fi
}


MONTH=$(date +%m)
YEAR=$(date +%y)
if [[ ${MONTH} -ge 01 ]] && [[ ${MONTH} -le 05 ]]
then
  spring(${YEAR})
	summer(${YEAR})
fi

if [[ ${MONTH} -ge 05 ]] && [[ ${MONTH} -le 09 ]]
then
	summer(${YEAR})
	fall(${YEAR})
fi

if [[ ${MONTH} -ge 09 ]] || [[ ${MONTH} -eq 01 ]]
then
	fall(${YEAR})
	spring(${YEAR})
fi