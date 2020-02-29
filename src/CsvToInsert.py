import glob, os
import csv
import re
import db.connection as connection
import io
from psycopg2.extras import RealDictCursor

class CsvToInsert:

    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def dayToNum(self, dayStr):
        if (dayStr == 'M'):
            return 0
        elif (dayStr == 'T'):
            return 1
        elif (dayStr == 'W'):
            return 2
        elif (dayStr == 'R'):
            return 3
        elif (dayStr == 'F'):
            return 4
        raise Exception(f"Invalid day code provided: {dayStr}")

    def getDays(self, daySequenceStr):
        return set(filter(lambda day: day, re.split("(?:(M|T|W|R|F))", daySequenceStr)))

    def populateDBFromCSVDataSourceDirectoryPath(self, files):
        if (type(files) is list and len(files) > 0):
            raw_conn = self.db.getConnection()
            with raw_conn.cursor(cursor_factory=RealDictCursor) as transaction:
                try:
                    defaultSemester = "Summer 2020"
                    defaultDateStart = "2020-01-01"
                    defaultDateEnd = "2020-01-01"
                    for raw_file in files:
                        csvfile = None
                        if (type(raw_file) == str and '.' in raw_file and raw_file.rsplit('.')[1] == 'csv') or (isinstance(raw_file, io.FileIO) and raw_file.filename and '.' in raw_file.filename and raw_file.filename.rsplit('.')[1] == 'csv') or isinstance(raw_file, io.StringIO):
                            if type(raw_file) == str or (isinstance(raw_file, io.FileIO) and raw_file.closed == True):
                                csvfile = open(raw_file, "r")
                            else:
                                csvfile = raw_file
                            print(csvfile)
                            # From the API endpoint, /api/upload or whatever the CSV upload is, the file objects will currently
                            # be StringIO. Cannot check the extension of this since it's a temp in-memory file. Will just let
                            # the error flow to the catch block.
                            reader = csv.DictReader(csvfile)
                            for row in reader:
                                days = self.getDays(row['course_days_of_the_week'])
                                # Change this if day of the week can be NULL
                                if (len(days) > 0):
                                    for day in days:
                                        transaction.execute(
                                            "INSERT INTO testCourseSession VALUES (%(CRN)s, %(Section)s, %(Semester)s, %(StartTime)s, %(EndTime)s, %(WeekDay)s);",
                                            {
                                                "CRN": row['course_crn'],
                                                "Section": row['course_section'],
                                                "Semester": defaultSemester,
                                                "StartTime": row['course_start_time'],
                                                "EndTime": row['course_end_time'],
                                                "WeekDay": self.dayToNum(day)
                                            }
                                        )
                                transaction.execute(
                                    "INSERT INTO testCourse VALUES (%(CRN)s, %(Section)s, %(Semester)s, %(StartDate)s, %(EndDate)s, %(Department)s, %(Level)s, %(Title)s);",
                                    {
                                        "CRN": row['course_crn'],
                                        "Section": row['course_section'],
                                        "Semester": defaultSemester,
                                        "StartDate": defaultDateStart,
                                        "EndDate": defaultDateEnd,
                                        "Department": row['course_department'],
                                        "Level": row['course_level'],
                                        "Title": row['course_name'],
                                    }
                                )
                        raw_conn.commit()
                except Exception as e:
                    print(e)
                    raw_conn.rollback()

# Test Driver
if __name__ == "__main__":
    os.chdir(os.path.abspath("../rpi-data"))
    fileNames = glob.glob("*.csv")
    insertJob = CsvToInsert(connection.db)
    insertJob.populateDBFromCSVDataSourceDirectoryPath(fileNames)
