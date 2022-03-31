# Tortoise Conversion

Here are some basic instructions for what we need to do for each layer in this conversion.

### Layers:

- Tests - Optional work. If you have the time or opt to for the sake of removing dependencies, you can verify tests with DB calls instead of secondary API calls.
- API (App.py) - Minimal work. Mainly adding await and asynchronous database calls
- Controller - Ideally minimal work. Responsible for verifying and cleaning data being inserted into the database
- DB - Probably the most work. Responsible for all SQL calls into the database.
- Tables/Models - Fairly straightforward, just converting from SQLAlchemy's Columns to Tortoise's Fields.

## Tests

- A new marker has been added for the sake of only running tests that don't rely on endpoints that have not yet been converted to the tortoise database.
- You can add tests to be executed by adding the marker @pytest.marker.tortoise to each test case you want to run
- If you opt to convert your tests over to use database calls instead of extra API calls, use the following resource to query from the database
    - https://tortoise-orm.readthedocs.io/en/latest/query.html
- You can also create new entries in the database with <model>.create(...) rather than posting new entries via the API, just make sure you are doing it correctly and preferrably removing entries after your test case finishes.
- Database calls are asynchronous so you can use the test fixture event_loop to run the calls
    - See the first test case in test_user.py for an example of this
- Clear your model in the conftest.py file. There is a clear_tables() function with examples of how to do this.
    
## API

- This layer is straightforward. The interface used should remain the same here. We will only need to await any database calls. Note that some cases try to manipulate the results of the query, you need to await the call, save it to a variable, and then you can manipulate it.
- This also means labeling any endpoints as asynchronous if not already marked as such.
- You will also need to uncomment/update any imports needed from the database layers.

## Controller

- If the other layers are done properly, there should not need to be any changes made to this layer besides awaiting calls into the db layer.
- If you do find yourself needing to make other types of changes, try fixing the other layers first.

## Tables/Models:

- For this layer, we want to move each table from the tables directory to the models directory.
- This means updating the __init__.py files in each directory. You can cut and paste the associated line for each table from the tables' init file to the models' init file.
- Update the imports for each model. Import tortoise fields and model. The new models should inherit from Model rather than Base.
- Update the Columns to Fields. Most conversions are straightforward, you can find the associated fields here: https://tortoise-orm.readthedocs.io/en/latest/fields.html
- Replace the table name with a subclass called Meta, as done in models/user_account.py
- Remove any no longer used imports.

## Testing your changes

- Once all layers needed for certain API calls are completed, you can test your work by simply adding the marker @pytest.mark.tortoise to any associated tests that we wrote in our FastAPI conversion.
- Run the tests on a test database by running  


    docker compose -f src/api/tests/docker-compose.yml up --build --abort-on-container-exit
    
- Only pay attention to errors raised directly by yacs_db_test and yacs_api_test. The --abort-on-container-exit is shutting down the db container when the tests finish which should leave a message like "ERRO[0008] 0" at the very end.


## Hints:

- If you run into any weird database issues where it is interpreting input as columns or something weird like that, try adding single quotes around the input (typically %s in the sql query string)
- If your sql query is selecting from or inserting into 'public.<table>' remove the 'public.'
- If your sql query consists of multiple commands, you will need to break it into two and run them seperately.
- If you want to see all query logs from the database, uncomment the last line in src/api/tests/docker-compose.yml and run again. This logs all queries made to the database, not just failed ones.
