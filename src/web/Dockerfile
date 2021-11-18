FROM node:16.13-alpine as develop-stage
USER node
WORKDIR /app
COPY --chown=node:node package*.json ./
RUN npm install
COPY --chown=node:node ./ .

FROM develop-stage as build-stage
RUN npm run build

FROM bunkerity/bunkerized-nginx:1.3.2 as production-stage
COPY --from=build-stage --chown=101:101 /app/dist /www
COPY nginx.redirects.conf /server-confs/nginx.redirects.conf
