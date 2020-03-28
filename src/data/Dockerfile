FROM library/postgres

# Copy migration files
COPY ./schema/ /home/schema/
COPY ./all.sql /home/

# Execute migrations files
COPY ./db_migration.sh /docker-entrypoint-initdb.d/

ENV POSTGRES_USER yacs
ENV POSTGRES_PASSWORD yacs_pass
ENV POSTGRES_DB yacs
