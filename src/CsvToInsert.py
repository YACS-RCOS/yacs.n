import glob, os
# import pandas as pd
import csv
import re

import db.connection as connection

class CsvToUpdate:

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def dayToNum(self, dayStr):
        if (dayStr == 'M'):
            return 0
        elif (dayStr == 'T'):
            return 1
        elif (dayStr == 'W'):
            return 2
        elif (dayStr == 'TR'):
            return 3
        elif (dayStr == 'F'):
            return 4
        raise Exception(f"Invalid day code provided: {dayStr}")

    def getDays(self, daySequenceStr):
        return list(filter(lambda day: day, re.split("(?:(M|(T^R?)|W|F))", daySequenceStr)))

    def populateDBFromCSVDataSourceDirectoryPath(self, csv_data_directory):
        os.chdir(csv_data_directory)
        courseInsertQueries = ''
        courseSessionInsertQueries = ''
        for file in glob.glob("*.csv"):
            with open(file, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                # parsed = pd.read_csv(csvfile)
                # print(parsed.head())
                # for row in parsed.iterrows():
                for row in reader:
                    defaultSemester = "Summer 2020"
                    defaultDateStart = "'2020-01-01'::date"
                    defaultDateEnd = "'2020-01-01'::date"
                    days = self.getDays(row['course_days_of_the_week']);
                    self.db_conn.
                    # Change this if day of the week can be NULL
                    if (len(days) > 1):
                        for day in days:
                            courseSessionInsertQueries += "\nINSERT INTO testCourseSession VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5});".format(row['course_crn'], row['course_section'], defaultSemester, row['course_start_time'], row['course_end_time'], self.dayToNum(day))
                            # self.db_conn.execute(

                            # )
                    courseInsertQueries += "\nINSERT INTO testCourse VALUES ('{0}', '{1}', '{2}', {3}, {4}, '{5}', {6}, '{7}');".format(row['course_crn'], row['course_section'], "Summer 2020", defaultDateStart, defaultDateEnd, row['course_department'], row['course_level'], row['course_name'])
                    # print(row.course_name)
        print(courseSessionInsertQueries)

if __name__ == "__main__":
    insertJob = CsvToUpdate(connection.db)
    insertJob.populateDBFromCSVDataSourceDirectoryPath(os.path.abspath("../rpi-data"))