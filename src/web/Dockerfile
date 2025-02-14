FROM node:13-alpine AS develop-stage
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY ./ .

FROM develop-stage AS build-stage
RUN npm run build

FROM bunkerity/bunkerized-nginx:1.3.2 AS production-stage
COPY --from=build-stage /app/dist /www
COPY nginx.redirects.conf /server-confs/nginx.redirects.conf
