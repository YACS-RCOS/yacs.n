FROM node:20-alpine as develop-stage
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY ./ .

FROM develop-stage as build-stage
RUN npm run build

FROM bunkerity/bunkerized-nginx:1.3.2 as production-stage
COPY --from=build-stage /app/dist /www
COPY nginx.redirects.conf /server-confs/nginx.redirects.conf
