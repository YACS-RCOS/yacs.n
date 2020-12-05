--
./scripts is dir for scripts to ease development and production deployments:
NOTE: All scripts must be run from project root

dev scripts:
------------
dev-create-migration.sh : Creates database migration using Alembic
dev-build.sh : Builds docker images locally and removes volumes
  NOTE! This will delete all data stored in the database
dev-start.sh : Starts docker containers for development, ctrl-c to stop containers
dev-stop.sh: Removes stopped containers
dev-start-legacy.sh : Starts /src/api and /src/web without docker (API and Vue frontend)

prod scripts:
-------------
start.sh : Starts production in background (with gunicorn with multiple workers, and hides ports to db and api)
stop.sh : Stops production background containers and removes data

usage guide:
------------
(windows users should use the corresponding .bat script e.g. instead of dev-start.sh do dev-start.bat)

If you have changed the schemas and would like to create a new database migration, run
        dev-create-migration.sh
  This will compare the state of the database to the defined schemas and automagically generate
  a migration script based on the changes. The migration can be found in `src/api/migrations/versions`.
  
  Then stop and restart `yacs_api` to apply the migration and update the database tables. 

If the web dependencies change, run: 
        dev-build.sh
  (NOTE! this will delete all data stored in the database)
  
    If the above command throws an error saying the volumes are in use, 
    run 
        dev-stop.sh
    and try again


To start developing, run: 
        dev-start.sh
    Changing code in `src/web` and `src/api` will automatically update the respective service

    To stop, press `ctrl-c` in the terminal that you are ran `dev-start.sh` in.
    The program should show each service exiting then exit.

When you finished developing, run:
        dev-stop.sh


TODO: channel CLI args to start.sh and dev-start.sh so that we can add root users and alt top level env vars