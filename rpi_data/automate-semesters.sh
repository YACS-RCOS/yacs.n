#!/usr/bin/env bash

spring() {
	local year=${1}
	source_url=https://sis.rpi.edu/reg/zfs${year}01.htm

	python3 ./website_checker.py ${source_url}
	exitCode=$?
	if [ ${exitCode} == 0 ]
	then
		export SEMESTER="SPRING ${year}"
		SOURCE_URL=${source_url} DEST=p0.csv HEADERS=True python3 ./modules/rpi-parse.py
		cat p* > spring-${year}.csv
		rm -rf p*.csv
		curl --insecure -X POST -H "Content-Type: multipart/form-data" -F "isPubliclyVisible=on" -F "file=spring-${year}" -A "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0" -k $API_ENDPOINT
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
		export SEMESTER="SUMMER ${year}"
		SOURCE_URL=${source_url_a} HEADERS=True DEST=p0.csv python3 ./modules/rpi-parse.py
		SOURCE_URL=${source_url_b} HEADERS=False DEST=p1.csv python3 ./modules/rpi-parse.py
		SOURCE_URL=${source_url_c} HEADERS=False DEST=p2.csv python3 ./modules/rpi-parse.py
		cat p* > summer-${year}.csv
		rm -rf p*.csv
		curl --insecure -X POST -H "Content-Type: multipart/form-data" -F "isPubliclyVisible=on" -F "file=summer-${year}" -A "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0" $API_ENDPOINT
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
		export SEMESTER="FALL ${year}"
		SOURCE_URL=${source_url} DEST=p0.csv HEADERS=True python3 ./modules/rpi-parse.py
		cat p* > fall-${year}.csv
		rm -rf p*.csv
		curl --insecure -X POST -H "Content-Type: multipart/form-data" -F "isPubliclyVisible=on" -F "file=fall-${year}" -A "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0" $API_ENDPOINT
	else
		echo "A requested Fall SIS page returned error 404." >&2
	fi
}


MONTH=$(date +%m)
YEAR=$(date +%Y)
API_ENDPOINT=https://yacs_web:8443/api/bulkCourseUpload
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

rm *.csv
