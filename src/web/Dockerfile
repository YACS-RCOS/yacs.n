FROM node:13-alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .

FROM develop-stage as build-stage
RUN npm run build

FROM bunkerity/bunkerized-nginx:latest as production-stage
# RUN mkdir /app
COPY --from=build-stage /app/dist /www
# COPY nginx.conf /etc/nginx/nginx.template.conf
COPY nginx.redirects.conf /server-confs/nginx.redirects.conf
# COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
# COPY cert/ /etc/nginx/cert

# RUN \
#   apt-get update --no-install-recommends && \
#   apt-get install openssl --no-install-recommends -y && \
#   rm -rf /var/lib/apt/lists/* || true

# CMD ["/usr/local/bin/entrypoint.sh"]
