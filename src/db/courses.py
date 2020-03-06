import glob
import os
import csv
import re
import db.connection as connection
from psycopg2.extras import RealDictCursor


class Courses:

    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def dayToNum(self, day_char):
        day_map = {
            'M': 0,
            'T': 1,
            'W': 2,
            'R': 3,
            'F': 4
        }
        day_num = day_map.get(day_char, -1)
        if day_num != -1:
            return day_num
        else:
            raise Exception("Invalid day code provided")

    def getDays(self, daySequenceStr):
        return set(filter(
            lambda day: day, re.split("(?:(M|T|W|R|F))", daySequenceStr)))

    def populate_from_csv(self, csv_text):
        conn = self.db.get_connection()
        reader = csv.DictReader(csv_text)
        for row in reader:
            # for each course entry insert sections and course sessions
            with conn.cursor(cursor_factory=RealDictCursor) as transaction:
                try:
                    # course sessions
                    days = self.getDays(row['course_days_of_the_week'])
                    if (len(days) > 0):
                        for day in days:
                            transaction.execute(
                                """
                                INSERT INTO
                                    course_session(
                                        crn,
                                        section,
                                        semester,
                                        time_start,
                                        time_end,
                                        day_of_week
                                    )
                                VALUES (
                                    %(CRN)s,
                                    %(Section)s,
                                    %(Semester)s,
                                    %(StartTime)s,
                                    %(EndTime)s,
                                    %(WeekDay)s
                                )
                                ON CONFLICT DO NOTHING;
                                """,
                                {
                                    "CRN": row['course_crn'],
                                    "Section": row['course_section'],
                                    "Semester": row['semester'],
                                    "StartTime": row['course_start_time'],
                                    "EndTime": row['course_end_time'],
                                    "WeekDay": self.dayToNum(day)
                                }
                            )
                    conn.commit()
                    # courses
                    transaction.execute(
                        """
                        INSERT INTO
                            course(
                                crn,
                                section,
                                semester,
                                date_start,
                                date_end,
                                department,
                                level,
                                title
                            )
                        VALUES (
                            %(CRN)s,
                            %(Section)s,
                            %(Semester)s,
                            %(StartDate)s,
                            %(EndDate)s,
                            %(Department)s,
                            %(Level)s,
                            %(Title)s
                        )
                        ON CONFLICT DO NOTHING;
                        """,
                        {
                            "CRN": row['course_crn'],
                            "Section": row['course_section'],
                            "Semester": row['semester'],
                            "StartDate": row['course_start_date'],
                            "EndDate": row['course_end_date'],
                            "Department": row['course_department'],
                            "Level": row['course_level'],
                            "Title": row['course_name'],
                        }
                    )
                    conn.commit()
                except Exception as e:
                    conn.commit()
                    print(e)


if __name__ == "__main__":
    # os.chdir(os.path.abspath("../rpi-data"))
    # fileNames = glob.glob("*.csv")
    csv_text = open('../../rpi-data/summer-2020.csv', 'r')
    courses = Courses(connection.db)
    courses.populate_from_csv(csv_text)
