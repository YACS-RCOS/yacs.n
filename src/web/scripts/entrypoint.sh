#!/usr/bin/env bash
# for use in docker image to start
# store pass with crypt(3) with openssl
mkdir -p /conf
CRYPT3_PASS=$(openssl passwd $ADMIN_PASS)

# add user:pass credentials for use in secured routes
echo "admin:$CRYPT3_PASS" >> /conf/htpasswd

# substitute env vars ex ${HOST} with HOST env var
# NOTE: must list all env vars explicilty here: https://github.com/docker-library/docs/issues/496
envsubst '\$HOST' < \
  /etc/nginx/nginx.template.conf > \
  /etc/nginx/nginx.conf

# start nginx
echo "starting nginx:"
nginx -g "daemon off;"
