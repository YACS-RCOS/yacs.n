
import csv
import json
from fastapi.encoders import jsonable_encoder
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
    global columns, crr
    columns = ["department", "courseCode", "section", "room", "dayofweek", "day", "hour"]
    crr = ["department", "courseCode", "section", "room", "dayOfWeek", "day", "hour"]

    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache
    
    def add_bulk_final(self, file):
        list = []
        for i in file:
            if i['Section'] == "(ALL SECTIONS)":
                section = "AllSections"
            else:
                section = i['Section']
            list.append(self.add_final(i['Department'], i['CourseCode'], section, i['Room'], i['DayOfWeek'], i['Day'], i['Hour']))
        self.clear_cache()
        return list, None

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
            return self.db_conn.execute("""
            INSERT INTO
                finals (department, "courseCode", section, room, "dayOfWeek", day, hour)
            VALUES
                   (%(department)s, %(courseCode)s, %(section)s, %(room)s, %(dayOfWeek)s, %(day)s, %(hour)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "department": department,
                "courseCode": courseCode,
                "section": section,
                "room": room,
                "dayOfWeek": dof,
                "day": day,
                "hour": hour
            }, False)

    def clear_cache(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.cache.clear(namespace="API_CACHE"))
        else:
            asyncio.run(self.cache.clear("API_CACHE"))

    def findCol(self, column):
        i=0
        for cols in columns:
            if cols.lower() == column:
                return (True, crr[i])
            i+=1
        return (False, column)
        
    def get_all_final_info(self):
        return self.db_conn.execute("SELECT * FROM finals;", None, True)
        
    def get_info_by_courseCode(self, courseCode):
        if courseCode is None:
            return(False, "Course Code cannot be none")
        return self.db_conn.execute("""
            SELECT * FROM finals WHERE "courseCode" = %(courseCode)s;
        """, {
            "courseCode": courseCode
        }, True)

    def get_info_by_courseCodeSection(self, courseCode, section):
        if courseCode is None:
            return(False, "Course Code cannot be none")
        elif section is None:
            return(False, "Section cannot be None")
        return self.db_conn.execute("""
            SELECT * FROM finals WHERE "courseCode" = %(courseCode)s AND section = %(section)s;
        """, {
            "courseCode": courseCode,
            "section": section
        }, True)
    
    def get_info_by_day(self, day):
        if day is None:
            return (False, "Date cannot be none")
        query = "SELECT * FROM finals WHERE day = \'" + day + "\';"
        return self.db_conn.execute(query, None, True)
    
    def get_info_by_department(self, department):
        if department is None:
            return(False, "Department cannot be none")
        query = "SELECT * FROM finals WHERE department = \'" + department + "\';"
        return self.db_conn.execute(query, None, True)
    
    def get_info_by_DOW(self, DOW):
        if DOW is None:
            return(False, "Day of Week cannot be none")
        return self.db_conn.execute("""
            SELECT * FROM finals WHERE "dayOfWeek" = %(DOW)s;
        """, {
            "DOW": DOW
        }, True)
    
    def get_info_by_hour(self, hour):
        if hour is None:
            return(False, "Hour cannot be None")
        query = "SELECT * FROM finals WHERE hour = \'" + hour + "\';"
        return self.db_conn.execute(query, None, True)
    
    def get_info_by_room(self, room):
        if room is None:
            return(False, "Room cannot be None")
        query = "SELECT * FROM finals WHERE room = \'" + room + "\';"
        return self.db_conn.execute(query, None, True)
    
    def remove_bulk_final(self, file):
        list = []
        for i in file:
            if i['Section'] == "(ALL SECTIONS)":
                section = "AllSections"
            else:
                section = i['Section']
            print("here1")
            print(i['CourseCode'])
            list.append(self.remove_final(i['CourseCode'], section))
            print("here")
        self.clear_cache()
        return list
    
    def remove_final(self, courseCode, section):
        self.clear_cache()
        return self.db_conn.execute("""
            BEGIN TRANSACTION;
                DELETE FROM finals
                WHERE "courseCode"=%(courseCode)s AND section=%(section)s;
            COMMIT;
        """, {
            "courseCode": courseCode,
            "section": section
        }, isSELECT=False)
        
    def update_final(self, courseCode, section, column : str, value : str):
        if courseCode is None:
            return (False, "CourseCode cannot be none")
        elif section is None:
            return (False, "Section cannot be none")
        
        error, column = self.findCol(column)
        if error:
            query = "UPDATE finals SET " + column + " = \'" + value + "\' WHERE courseCode = \'" + courseCode + "\' AND section = \'" + section + "\';"
            return self.db_conn.execute(query, None, True)
        else:
            return (False, "Column does not exist")