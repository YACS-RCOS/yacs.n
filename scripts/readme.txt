--
./scripts is dir for scripts to ease development and production deployments:
NOTE: All scripts must be run from project root

dev scripts:
------------
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
(windows users should use the corresponding .bat script e.g. instead of dev-build.sh do dev-build.bat)

1) If any of the following are true
  - first time setup
  - database tables changed
  - web dependencies changed

  Run: 
        dev-build.sh 
  (this will delete all data stored in the database)

2) To start developing, run: 
        dev-start.sh
    Changing code in `src/web` and `src/api` will automatically update the respective service

    To stop, press `ctrl-c` in the terminal that you are ran `dev-start.sh` in.
    The program should show each service exiting then exit.



TODO: channel CLI args to start.sh and dev-start.sh so that we can add root users and alt top level env vars