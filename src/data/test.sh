#!/usr/bin/env bash
echo '-- build db --'
bash build.sh

echo '-- seed db --'
bash seed.sh

echo '-- run test queries --'
for query in queries/*
do
  psql -d yacs < $query
done
