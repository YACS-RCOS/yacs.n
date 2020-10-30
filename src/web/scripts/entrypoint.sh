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


# If SSL Certificate folder isn't present, generate one
if [ ! -f /etc/nginx/certificate/$HOST.crt ] &&
[ ! -f /etc/nginx/certificate/$HOST.csr ] &&
[ ! -f /etc/nginx/certificate/$HOST.key ];then
  mkdir /etc/nginx/certificate
  cd /etc/nginx/certificate
  openssl genrsa -passout pass:x -out $HOST.pass.key 2048
  openssl rsa -passin pass:x -in $HOST.pass.key -out $HOST.key
  rm $HOST.pass.key
  openssl req -new -key $HOST.key -out $HOST.csr -subj "/C=US/ST=New York/O=RPI RCOS"
  openssl x509 -req -days 365 -in $HOST.csr -signkey $HOST.key -out $HOST.crt
fi

# start nginx
echo "starting nginx:"
nginx -g "daemon off;"
