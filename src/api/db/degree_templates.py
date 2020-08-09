import glob
import os
import csv
import re
import json
from psycopg2.extras import RealDictCursor
from ast import literal_eval

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection

class DegreeTemplates:
    def __init__(self, db_wrapper, cache):
        self.db = db_wrapper
        self.cache = cache  
    
    def parse(self, data):
        self.id = degree + "_" + major  + "_" + year
        self.degree = data["degree"]
        self.major = data["major"]
        self.year = data["year"]
        self.template = str(data["semesters"])
        
    def insert_into_db(self, transaction):
        #convert json as text and insert it as text type instead of varchar
        transaction.execute("""
            INSERT INTO degree_template(
                id,
                degree,
                major,
                year,
                template
            ) VALUES (
                %(id)s,
                %(degree)s,
                %(major)s,
                %(year)d,
                %(template)s,
            )
            ON CONFLICT DO NOTHING;
        """,
        {
            "id": self.id,
            "degree": self.degree,
            "major": self.major,
            "year" : self.year,
            "template" : self.info
            
        });
    
   
    # taking in degree template json file and inserting into database
    def import_degree_template(data: str):
      # taking in raw data, parsing it into objects
        degree_template_JSON = json.load(data)
        degreeTemplate = DegreeTemplate.parse(degree_template_JSON)
     # after parsing all the parts into objects, insert objects into database
        db_conn = self.db.connection()
        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            DegreeTemplate.insert_into_db(transaction)
            
if __name__ == "__main__":
    # os.chdir(os.path.abspath("../rpi_data"))
    # fileNames = glob.glob("*.csv")
    json_text = open('../../../rpi_data/fall-2020.csv', 'r')
    courses = Courses(connection.db)
    courses.insert_into_db(json_text)