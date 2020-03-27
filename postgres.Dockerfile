FROM library/postgres

# Copy migration files
COPY ./src/data/schema/ /home/schema
COPY ./all.sql /home

# Execute migrations files
COPY ./scripts/db_migration.sh /docker-entrypoint-initdb.d/

ENV POSTGRES_USER yacs
ENV POSTGRES_PASSWORD yacs_pass
ENV POSTGRES_DB yacs
