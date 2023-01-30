FROM node:13-alpine as develop-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY ./ .

FROM develop-stage as build-stage
RUN npm run build

FROM build-stage as production-stage
COPY --from=build-stage /app/dist /www
COPY nginx.redirects.conf /server-confs/nginx.redirects.conf
