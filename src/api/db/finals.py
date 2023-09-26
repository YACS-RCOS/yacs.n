import csv
import json
from psycopg2.extras import RealDictCursor
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from your_module import Professor, Base

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection

class Professor:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def add_final(self, department, courseCode,
                  section, room, dof, day, hour):
        if department is None:
            return (False, "Department cannot be none")
        elif courseCode is None:
            return (False, "Course code cannot be none")
        elif section is None:
            return (False, "Section cannot be none")
        elif room is None:
            return (False, "Room cannot be none")
        elif dof is None:
            return (False, "Day of Week cannot be none")
        elif day is None:
            return (False, "Day cannot be none")
        elif hour is None:
            return (False, "Hour cannot be none")
        else:
            query = "INSERT INTO finals VALUES(%s, %s, %s, %s, %s, %s, %s);"
            values = (department, courseCode, section, room, dof, day, hour)
            cursor = self.db_conn.cursor()
            return cursor.execute(query, values)
        
    def add_professor(self, first_name, last_name, email, phone, dep, office, 
        classes, office_time, rcs):
            if email is not None:
                print(email)
                return self.db_conn.execute("""
            INSERT INTO 
                professor (first_name, last_name, email, phone_number, 
                department, office_room, classes, office_hours_time, rcs)
            VALUES 
                   (%(First_name)s, %(Last_name)s, %(Phone_number)s, %(Email)s,
                   %(Dep)s, %(Office_room)s, %(Classes)s, %(Office_time)s, %(Rcs_id)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "First_name": first_name,
                "Last_name": last_name,
                "Email": email, 
                "Phone_number": phone,
                "Dep": dep, 
                "Office_room": office, 
                "Classes": classes,
                "Office_time": office_time,
                "Rcs_id": rcs
            }
        , False)
            else:
                return (False, "email cant be none")



def add_bulk_professor(self):
    # Load the JSON data from a file
    with open('Professors.json') as file:
        data = json.load(file)

    # Connect to the SQL database
    conn = self.db.get_connection()

    # Loop through each professor record in the JSON data
    for record in data:
        professor = Professor(email=record['Email'],
                            first_name=record['Name'],
                            phone_number=record['Phone'],
                            department=record['Department'],
                            office_room=record['Portfolio'],
                            office_hours_time='',
                            rcs='')
        conn.add(professor)

    # Commit the changes to the database
    conn.commit()
    self.clear_cache()
    return (True,None)


    
if __name__ == "__main__":
    csv_text = open('../../../rpi_data/fall-2020.csv', 'r')
    courses = Professor(connection.db)
    courses.populate_from_csv(csv_text)