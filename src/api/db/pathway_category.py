import csv
import json
from psycopg2.extras import RealDictCursor
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

##!!!!!!!!!!!!!!!!!!!!
## TO UPDATE WITH NEW PATHWAYS/CATEGORIES, CHANGE JSON FILE AT BOTTOM OF PAGE
##!!!!!!!!!!!!!!!!!!!!

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection


class Pathway_Category:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def add_category(self, category_name):
        if category_name is not None:
            print(category_name)
            return self.db_conn.execute("""
            INSERT INTO
                pathway_category (category_name)
            VALUES
                   (%(pathway_name)s, %(category_name)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "category_name": category_name
            }, False)
        else:
            return (False, "category_name cannot be none")

    def add_bulk_category(self, json_data):  # function is called in app.py
        # Connect to the SQL database
        conn = self.db_conn.get_connection()

        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                # Iterate over each entry in the JSON data
                for entry in json_data:
                    try:

                        # Insert category into "pathway_category" table (tables/pathways_category.py)
                        transaction.execute(
                            """
                            INSERT INTO pathway_category (
                                category_name
                            )
                            VALUES (
                                NULLIF(%(category_name)s, '')  
                            )
                            ON CONFLICT DO NOTHING;
                            """,
                            {
                                "category_name": entry['Category Name'][0]
                             }
                        )
                    except Exception as e:
                        # Roll back the transaction and return the exception if an error occurs
                        print("THIS IS THE EXCEPTION: pathway_category", e)
                        conn.rollback()
                        return (False, e)
            except ValueError as ve:
                # Return an error message if the JSON data is invalid
                return (False, f"Invalid JSON data: {str(ve)}")

            # Commit the transaction if all entries are inserted successfully
            conn.commit()

            # Invalidate cache to ensure new data is retrieved
            # self.clear_cache()

            # Return success status and no error
            return True, None


def clear_cache(self):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        loop.create_task(self.cache.clear(namespace="API_CACHE"))
    else:
        asyncio.run(self.cache.clear("API_CACHE"))


if __name__ == "__main__":
    pathways = Pathway_Category(connection.db)
    pathways.add_bulk_category('../../../src/web/src/pages/pathwayV2.json')  # CHANGE FILE HERE IF NEEDED
