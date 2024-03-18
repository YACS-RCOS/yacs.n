FROM docker.io/node:current-alpine as develop-stage

# this should be the path to the volume defined in docker-compose
WORKDIR /app

COPY package*.json ./
RUN npm ci

FROM develop-stage as build-stage
RUN npm run build

FROM docker.io/bunkerity/bunkerized-nginx:1.3.2 as production-stage
COPY --from=build-stage /app/dist /www
COPY nginx.redirects.conf /server-confs/nginx.redirects.conf
