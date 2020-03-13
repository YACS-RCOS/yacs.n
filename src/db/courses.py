import glob
import os
import csv
import re
from psycopg2.extras import RealDictCursor

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection


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
        # for each course entry insert sections and course sessions
        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            for row in reader:
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
                                        day_of_week,
                                        location
                                    )
                                VALUES (
                                    NULLIF(%(CRN)s, ''),
                                    NULLIF(%(Section)s, ''),
                                    NULLIF(%(Semester)s, ''),
                                    %(StartTime)s,
                                    %(EndTime)s,
                                    %(WeekDay)s,
                                    NULLIF(%(Location)s, '')
                                )
                                ON CONFLICT DO NOTHING;
                                """,
                                {
                                    "CRN": row['course_crn'],
                                    "Section": row['course_section'],
                                    "Semester": row['semester'],
                                    "StartTime": row['course_start_time'] if row['course_start_time'] and not row['course_start_time'].isspace() else None,
                                    "EndTime": row['course_end_time'] if row['course_end_time'] and not row['course_end_time'].isspace() else None,
                                    "WeekDay": self.dayToNum(day) if day and not day.isspace() else None,
                                    "Location": row['course_location']
                                }
                            )
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
                            NULLIF(%(CRN)s, ''),
                            NULLIF(%(Section)s, ''),
                            NULLIF(%(Semester)s, ''),
                            %(StartDate)s,
                            %(EndDate)s,
                            NULLIF(%(Department)s, ''),
                            %(Level)s,
                            NULLIF(%(Title)s, '')
                        )
                        ON CONFLICT DO NOTHING;
                        """,
                        {
                            "CRN": row['course_crn'],
                            "Section": row['course_section'],
                            "Semester": row['semester'],
                            "StartDate": row['course_start_date'] if row['course_start_date'] and not row['course_start_date'].isspace() else None,
                            "EndDate": row['course_end_date'] if row['course_end_date'] and not row['course_end_date'].isspace() else None,
                            "Department": row['course_department'],
                            "Level": row['course_level'] if row['course_level'] and not row['course_level'].isspace() else None,
                            "Title": row['course_name']
                        }
                    )
                except Exception as e:
                    conn.rollback()
                    return (False, e)
        conn.commit()
        return (True, None)


if __name__ == "__main__":
    # os.chdir(os.path.abspath("../rpi-data"))
    # fileNames = glob.glob("*.csv")
    csv_text = open('../../rpi-data/fall-2020.csv', 'r')
    courses = Courses(connection.db)
    courses.populate_from_csv(csv_text)
