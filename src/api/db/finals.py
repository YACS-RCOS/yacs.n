
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

class Finals:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def add_bulk_final(self, file):
        list = []

        #file  = "Finals.json"
        with open(file, "r") as json_file:
            data = json.load(json_file)

        for i in data:
            if i['Section'] == "(ALL SECTIONS)":
                section = "AllSections"
            else:
                section = i['Section']
            list.append(self.add_final(i['Department'], i['CourseCode'], section, i['Room'], i['DayOfWeek'], i['Day'], i['Hour']))
        self.db_conn.commit()
        self.clear_cache()
        return list

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
            return(False, "A record with the Course Code" + courseCode + " and Section = " + section + " already exists")
        else:
            query = "INSERT INTO finals VALUES(%s, %s, %s, %s, %s, %s, %s);"
            values = (department, courseCode, section, room, dof, day, hour)
            cursor = self.db_conn.cursor()
            info, error = cursor.execute(query, values, True)
            return (info, None) if not error else (False, error)
        
    def clear_cache(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.cache.clear(namespace="API_CACHE"))
        else:
            asyncio.run(self.cache.clear("API_CACHE"))
        
    def get_all_final_info(self):
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals;"
        info, error = cursor.execute(query, None, True)
        return (info, None) if not error else (False, error)

    def get_info_by_courseCode(self, courseCode):
        if courseCode is None:
            return(False, "Course Code cannot be none")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE CourseCode = \'" + courseCode + "\';"
        info, error = cursor.execute(query, None, True)
        return (info, None) if not error else (False, error)

    def get_info_by_courseCodeSection(self, courseCode, section):
        if courseCode is None:
            return(False, "Course Code cannot be none")
        elif section is None:
            return(False, "Section cannot be None")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE CourseCode = \'" + courseCode + "\' AND Section = " + section + ";"
        info, error = cursor.execute(query, None, True)
        return (info, None) if not error else (False, error)
    
    def get_info_by_day(self, day):
        if day is None:
            return (False, "Date cannot be none")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE Day = \'" + day + "\';"
        info, error = cursor.execute(query, None, True)
        return (info, None) if not error else (False, error)
    
    def get_info_by_department(self, department):
        if department is None:
            return(False, "Department cannot be none")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE Deparment = \'" + department + "\';"
        info, error = cursor.execute(query, None, True)
        return (info, None) if not error else (False, error)
    
    def get_info_by_DOW(self, DOW):
        if DOW is None:
            return(False, "Day of Week cannot be none")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE DayOfWeek = \'" + DOW + "\';"
        info, error = cursor.execute(query, None, True)
        return (info, None) if not error else (False, error)
    
    def get_info_by_hour(self, hour):
        if hour is None:
            return(False, "Hour cannot be None")
        cursor = self.db_conn.cursor()
        query = "SELECT * FROM finals WHERE Hour = \'" + hour + "\';"
        info, error = cursor.execute(query, None, True)
        return (info, None) if not error else (False, error)
        
    def remove_final(self, courseCode, section):
        if courseCode is None:
            return (False, "Course Code cannot be none")
        elif section is None:
            return (False, "Section cannot be none")
        
        query = "DELETE FROM finals WHERE CourseCode = \'" + courseCode + "\' AND Section = \'" + section + "\';"

        cursor = self.db_connect_cursor()
        info, error = cursor.execute(query, None, True)
        message = ""
        if not error:
            message = str(cursor.rowcount) + " row(s) deleted"
        
        return(message, None) if not error else (False, error)
    


