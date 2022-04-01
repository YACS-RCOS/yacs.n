# How to run API tests

Tests can be run using docker compose.  
Make sure you have docker desktop running and run the following command from the yacs.n directory.  

    docker-compose -f src/api/tests/docker-compose.yml up --build
    
This will run two containers, the database container and the test container.
The database will not stop running when the tests exit, but you can add the flag --abort-on-container-exit to do this.
This will leave an error message at the end that you can ignore.

The output from your tests should be logged in the yacs_api_test container.