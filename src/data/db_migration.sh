#!/usr/bin/env bash
ls /home/schema
for sqlschemacreate in /home/schema/; do
  psql -U yacs -p yacs_pass -d yacs -f $sqlschemacreate
done
