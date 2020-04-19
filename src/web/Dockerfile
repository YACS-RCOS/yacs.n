FROM node:13-alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .

FROM develop-stage as build-stage
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.template.conf
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh

# get openssl to do crypt(3)
RUN \
  apt-get update --no-install-recommends && \
  apt-get install openssl -y && \
  rm /var/lib/apt/lists/* || true

CMD ["/usr/local/bin/entrypoint.sh"]
