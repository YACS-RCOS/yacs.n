#!/usr/bin/env bash

spring() {
	local year=${1}
	source_url=https://sis.rpi.edu/reg/zfs${year}01.htm

	python3 ./website_checker.py ${source_url}
	exitCode=$?
	if [ ${exitCode} == 0 ]
	then
			echo "Spring"
			export SEMESTER="SPRING ${year}"
			DEST=p0.csv HEADERS=True DEST=p0.csv python3 ./modules/rpi-parse.py
			cat p* > spring-${year}.csv
			rm -rf p*.csv
	else
			echo "The requested Spring SIS page returned error 404." >&2
	fi
}

summer() {
	local year=${1}
	source_url_a=https://sis.rpi.edu/reg/zfs${year}05.htm
	source_url_b=https://sis.rpi.edu/reg/zfs${year}0502.htm
	source_url_c=https://sis.rpi.edu/reg/zfs${year}0503.htm

	python3 ./website_checker.py ${source_url_a} ${source_url_b} ${source_url}
	exitCode=$?
	if [ ${exitCode} == 0 ]
  then
  		echo "Summer"
			export SEMESTER="SUMMER ${year}"
			SOURCE_URL=${source_url_a} HEADERS=True DEST=p0.csv python3 ./modules/rpi-parse.py
			SOURCE_URL=${source_url_b} HEADERS=False DEST=p1.csv python3 ./modules/rpi-parse.py
			SOURCE_URL=${source_url_c} HEADERS=False DEST=p2.csv python3 ./modules/rpi-parse.py
			cat p* > summer-${year}.csv
			rm -rf p*.csv
	else
			echo "A requested Summer SIS page returned error 404." >&2
	fi
}

fall() {
	local year=${1}
	source_url=https://sis.rpi.edu/reg/zfs${year}09.htm
	
	python3 ./website_checker.py ${source_url}
	exitCode=$?
	if [ ${exitCode} == 0 ]
	then
			echo "Fall"
			export SEMESTER="FALL ${year}"
			DEST=p0.csv HEADERS=True DEST=p0.csv python3 ./modules/rpi-parse.py
			cat p* > fall-${year}.csv
			rm -rf p*.csv
	else
			echo "A requested Fall SIS page returned error 404." >&2
	fi
}


MONTH=$(date +%m)
YEAR=$(date +%Y)
if [[ ${MONTH} -ge 1 && ${MONTH} -lt 5 ]]
then
  spring ${YEAR}
	summer ${YEAR}
fi

if [[ ${MONTH} -ge 5 && ${MONTH} -lt 9 ]]
then
	summer ${YEAR}
	fall ${YEAR}
fi

if [[ ${MONTH} -ge 9 && ${MONTH} -le 12 ]]
then
	fall ${YEAR}
	spring ${YEAR}
fi