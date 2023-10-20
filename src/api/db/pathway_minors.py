import csv
import json
from psycopg2.extras import RealDictCursor
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection


class PathwayMinors:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def add_pathway_minor(self, minor, pathway):
        if minor is not None:
            print(minor)
            return self.db_conn.execute("""
            INSERT INTO
                pathway_minors (minor, pathway)
            VALUES
                   (%(minor)s, %(pathway)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "minor": minor,
                "pathway": pathway

            }, False)
        else:
            return (False, "minor cannot be none")

    def add_bulk_pathway_minors(self, json_data): #function is called in app.py
        # Connect to the SQL database
        conn = self.db_conn.get_connection()

        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                # Iterate over each entry in the JSON data
                for entry in json_data:
                    for sub in entry['Pathways']:
                        if 'Compatible minor(s)' in sub.keys():
                            for min in sub['Compatible minor(s)']:
                                try:
                                    # Insert pathways and corresponding category into "pathway" table (tables/pathways.py)
                                    transaction.execute(
                                        """
                                        INSERT INTO pathway_minors (
                                            minor,
                                            pathway

                                        )
                                        VALUES (
                                            NULLIF(%(minor)s, ''),
                                            NULLIF(%(pathway)s, '')
                                        )
                                        ON CONFLICT DO NOTHING;
                                        """,
                                        {
                                            "pathway": sub['Name'][0],
                                            "minor": min
                                        }
                                    )
                                except Exception as e:
                                    # Roll back the transaction and return the exception if an error occurs
                                    print("THIS IS THE EXCEPTION:", e)
                                    conn.rollback()
                                    return (False, e)
            except ValueError as ve:
                # Return an error message if the JSON data is invalid
                return (False, f"Invalid JSON data: {str(ve)}")

            # Commit the transaction if all entries are inserted successfully
            conn.commit()

            # Invalidate cache to ensure new data is retrieved
            self.clear_cache()

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
    minor = Pathway_minors(connection.db)
    minor.add_bulk_pathway_minor('../../../src/web/src/pages/pathwayV2.json') #CHANGE FILE HERE IF NEEDED
