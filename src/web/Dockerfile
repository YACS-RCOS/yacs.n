FROM node:13-alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .
RUN chown -R 101:101 cert

FROM develop-stage as build-stage
RUN npm run build

FROM bunkerity/bunkerized-nginx:1.3.2 as production-stage
COPY --from=build-stage /app/dist /www
COPY nginx.redirects.conf /server-confs/nginx.redirects.conf
