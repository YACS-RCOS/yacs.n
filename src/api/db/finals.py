'''
add_final - Sam
add_bulk_final - Sam
* remove_final - Sam
* clear_cache - Sam
* bulk_delete - Sam
* get_info_by_courseCode - Sam
* get_info_by_courseCodeSection - Abdul
* get_info_by_department - Abdul
* get_info_by_date - Abdul
* get_info_by_DOW - Abdul
* get_all_final_info - Abdul
* 
'''



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
        cursor = self.db_conn.cursor()
        query = "SELECT COUNT(*) FROM finals WHERE CourseCode = \'" + courseCode + "\' AND Section = " + str(section) + ";"
        cursor.execute(query)
        records = cursor.fetchone()
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
        elif (records[0] > 0):
            return(False, "A record with the same Course Code and Section exists")
        else:
            query = "INSERT INTO finals VALUES(%s, %s, %s, %s, %s, %s, %s);"
            values = (department, courseCode, section, room, dof, day, hour)
            cursor = self.db_conn.cursor()
            cursor.execute(query, values)
            self.db_conn.commit()
            return(True, "Final has been added")
        
    def get_all_final_info(self):
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals;"
        cursor.execute(query)
        return cursor.fetchall()

    def get_info_by_courseCode(self, courseCode):
        if courseCode is None:
            return(False, "Course Code cannot be none")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE CourseCode = \'" + courseCode + "\';"
        cursor.execute(query)
        return cursor.fetchall()

    def get_info_by_courseCodeSection(self, courseCode, section):
        if courseCode is None:
            return(False, "Course Code cannot be none")
        elif section is None:
            return(False, "Section cannot be None")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE CourseCode = \'" + courseCode + "\' AND Section = " + section + ";"
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_info_by_day(self, day):
        if day is None:
            return (False, "Date cannot be none")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE Day = \'" + day + "\';"
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_info_by_department(self, department):
        if department is None:
            return(False, "Department cannot be none")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE Deparment = \'" + department + "\';"
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_info_by_DOW(self, DOW):
        if DOW is None:
            return(False, "Day of Week cannot be none")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE DayOfWeek = \'" + DOW + "\';"
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_info_by_hour(self, hour):
        if hour is None:
            return(False, "Hour cannot be None")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE Hour = \'" + hour + "\';"
        cursor.execute(query)
        return cursor.fetchall()
        
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