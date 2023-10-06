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


class Pathway:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def add_pathway(self, pathway_name, category_name):
            if pathway_name is not None:
                print(pathway_name)
                return self.db_conn.execute("""
            INSERT INTO
                pathway (pathway_name, category_name)
            VALUES
                   (%(Pathway_name)s, %(Category_name)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "Pathway_name": pathway_name,
                "Category_name": category_name
            }
        , False)
            else:
                return (False, "pathway_name cannot be none")



    def add_bulk_pathways(self):
        # Load the JSON data from a file
        with open('../../web/src/pages/pathwayV2.json') as file:
            data = json.load(file)

        # Connect to the SQL database
        conn = self.db.get_connection()

        # Loop through each pathways in json file
        try:
            for category in data:
                for pathway in category['Pathways']:
                    pathway = Pathway(pathway_category = category["Category Name"][0],
                                      pathway_name = pathway["Name"][0])
                    conn.add(pathway)

            # Commit the changes to the database
            conn.commit()
            self.clear_cache()
            return (True,None)
        except Exception as e:
            print("THIS IS THE EXCEPTION:", e)
            conn.rollback()
            return (False, e)



# if __name__ == "__main__":
#     csv_text = open('../../../src/web/src/pages/pathwayV2.json', 'r')
#     pathways = Pathway(connection.db)
#     pathways.populate_from_csv(csv_text)

#add_bulk_pathways()
