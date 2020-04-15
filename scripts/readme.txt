--
./scripts is dir for scripts to ease development and production deployments:
NOTE: All scripts must be run from project root

dev scripts:
------------

dev-build.sh : Builds docker images locally for faster start (uses volumes to link storage in container with host storage on start)
dev-start.sh : Starts docker containers for development, ctrl c to stop containers
dev-stop.sh: Removes stopped containers
dev-start-legacy.sh : Starts /src/api and /src/web (API and Vue frontend)

prod scripts:
-------------
start.sh : Starts production in background (with gunicorn with multiple workers, and hides ports to db and api)
stop.sh : Stops production background containers and removes data

TODO: channel CLI args to start.sh and dev-start.sh so that we can add root users and alt top level env vars
