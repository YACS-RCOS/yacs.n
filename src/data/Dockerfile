FROM postgres:latest
# Copy migration files
COPY ./schema/ /docker-entrypoint-initdb.d/
# Execute migrations files on postres start
# ADD ./db_migration.sh
# RUN cat /docker-entrypoint-initdb.d/db_migration.sh

ENV POSTGRES_PASSWORD=yacs_pass
ENV POSTGRES_DB=yacs
ENV POSTGRES_USER=yacs
