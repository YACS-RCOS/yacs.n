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

class DegreeTemplate:
    def __init__(self, db_wrapper):
        self.db_conn = db_wrapper
    
    def parse(self, data):
        self.id = data["degree"] + "-" + data["major"]  + "-" + str(data["year"])
        self.degree = data["degree"]
        self.major = data["major"]
        self.year = data["year"]
        self.template = json.dumps(data["semesters"])
    
        
    def insert_into_db(self, transaction):
        print ("!!!!!!!!LOOK" + self.template)
        #try:
            #convert json as text and insert it as text type instead of varchar
        transaction.execute("""
            INSERT INTO degree_templates(
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
            "template" : self.template
            
        });
        #except Exception as e:
           # print(e)
            #return (False, e)
   
    # taking in degree template json file and inserting into database

    def import_degree_template(self, data):
      # taking in raw data, parsing it into objects
        #degree_template_JSON = json.load(data)
        degreeTemplate = self.parse(data)
     # after parsing all the parts into objects, insert objects into database
        db_conn = self.db_conn.get_connection()
        with db_conn.cursor(cursor_factory=RealDictCursor) as transaction:
            self.insert_into_db(transaction)
        
        db_conn.commit()
        # invalidate cache so we can get new classes
        #self.cache.clear()
        return (True, None)
    
    
   
    def get_template(self):
        return self.db_conn.execute("""
            select
                *
            from
                degree_templates
        """, None, True)
        
    def get_template_demo(self):
        json_file = open('../../rpi_data/graduation-requirement/Template/UN-CSCI-2019.json', 'r')
        json_text = json.load(json_file)
        json_file.close()
        return [json_text]
            
if __name__ == "__main__":
    # os.chdir(os.path.abspath("../rpi_data"))
    # fileNames = glob.glob("*.csv")
    json_text = open('../../../rpi_data/graduation-requirement/Template/UN-CSCI-2019.json', 'r') 
    courses = Courses(connection.db)
    courses.import_degree_template(json_text)
    