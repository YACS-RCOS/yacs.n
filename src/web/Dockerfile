FROM docker.io/oven/bun:latest as develop-stage

# this should be the path to the volume defined in docker-compose
WORKDIR /app

COPY package*.json ./
RUN bun i
COPY . ./

FROM develop-stage as build-stage
RUN bun run build

FROM docker.io/bunkerity/bunkerized-nginx:1.3.2 as production-stage
COPY --from=build-stage /app/dist /www
COPY nginx.redirects.conf /server-confs/nginx.redirects.conf
