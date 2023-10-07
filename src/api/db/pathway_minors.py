import csv
import json
from psycopg2.extras import RealDictCursor
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#from your_module import Professor, Base

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection

class pathway_minors:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

def add_bulk_minor(self):
    # Load the JSON data from a file
    with open('../../web/src/pages/pathwayV2.json') as file:
        data = json.load(file)

    # Connect to the SQL database
    conn = self.db.get_connection()

    for record in data:
        for p in i['Pathways']:
            if 'Compatible minor(s)' in p.keys():
                for min in p['Compatible minor(s)']:
                    print(min)
                    print(p['Name'][0])
                    minor = pathway_minors(pathway=p['Name'][0],
                                            minor=min
                                            )
                    conn.add(minor)
        # Commit the changes to the database
    conn.commit()
    self.clear_cache()
    return (True, None)

add_bulk_minor()