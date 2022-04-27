#!/usr/bin/env bash
export DB_HOST=${DB_HOST:-localhost}
export DB_USER=${DB_USER:-yacs}
export DB_PASS=${DB_PASS:-easy_dev_pass}
export DB_NAME=${DB_NAME:-yacs}
export DB_PORT=${DB_PORT:-5432}
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export TEST_APP_DIR=$SCRIPT_DIR/../

python3 -m pytest -s "${SCRIPT_DIR}"
