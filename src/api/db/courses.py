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

    def delete_by_semester(self, semester):
        return self.db.execute("""
            BEGIN TRANSACTION;
                DELETE FROM course
                WHERE semester=%(Semester)s;
                DELETE FROM course_session
                WHERE semester=%(Semester)s;
            COMMIT;
        """, {
            "Semester": semester
        }, isSELECT=False)

    def bulk_delete(self, semesters):
        for semester in semesters:
            _, error = self.delete_by_semester(semester)
            if error:
                print(error)
                return error
        return None

    def populate_from_csv(self, csv_text):
        conn = self.db.get_connection()
        reader = csv.DictReader(csv_text)
        # for each course entry insert sections and course sessions
        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            for row in reader:
                try:
                    # course sessions
                    days = self.getDays(row['course_days_of_the_week'])
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
                                    description,
                                    frequency,
                                    full_title,
                                    date_start,
                                    date_end,
                                    department,
                                    level,
                                    title,
                                    raw_precoreqs,
                                    tsv
                                )
                            VALUES (
                                NULLIF(%(CRN)s, ''),
                                NULLIF(%(Section)s, ''),
                                NULLIF(%(Semester)s, ''),
                                NULLIF(%(Description)s, ''),
                                NULLIF(%(Frequency)s, ''),
                                NULLIF(%(FullTitle)s, ''),
                                %(StartDate)s,
                                %(EndDate)s,
                                NULLIF(%(Department)s, ''),
                                %(Level)s,
                                NULLIF(%(Title)s, ''),
                                NULLIF(%(RawPrecoreqText)s, ''),
                                setweight(to_tsvector(coalesce(%(FullTitle)s, '')), 'A') || 
                                setweight(to_tsvector(coalesce(%(Title)s, '')), 'A') || 
                                setweight(to_tsvector(coalesce(%(Department)s, '')), 'A') || 
                                setweight(to_tsvector(coalesce(%(CRN)s, '')), 'A') || 
                                setweight(to_tsvector(coalesce(%(Level)s, '')), 'B') || 
                                setweight(to_tsvector(coalesce(%(Description)s, '')), 'D')
                            )
                            ON CONFLICT DO NOTHING;
                            """,
                            {
                                "CRN": row['course_crn'],
                                "Section": row['course_section'],
                                "Semester": row['semester'],
                                "Description": row['description'], # new
                                "Frequency": row['offer_frequency'], # new
                                "FullTitle": row["full_name"], # new
                                "StartDate": row['course_start_date'] if row['course_start_date'] and not row['course_start_date'].isspace() else None,
                                "EndDate": row['course_end_date'] if row['course_end_date'] and not row['course_end_date'].isspace() else None,
                                "Department": row['course_department'],
                                "Level": row['course_level'] if row['course_level'] and not row['course_level'].isspace() else None,
                                "Title": row['course_name'],
                                "RawPrecoreqText": row['raw_precoreqs']
                            }
                        )
                    # populate prereqs table, must come after course population b/c ref integrity
                    # Everything from the CSV comes in as a string,
                    # but this field is meant to be a list. TODO, what's
                    # a better way to get around this?
                    # ast.literal_eval will throw SyntaxError if given an empty string
                    prereqs = literal_eval(row['prerequisites']) if row['prerequisites'] else []
                    for prereq in prereqs:
                        transaction.execute(
                            """
                            INSERT INTO course_prerequisite (
                                department,
                                level,
                                prerequisite
                            )
                            VALUES (
                                NULLIF(%(Department)s, ''),
                                %(Level)s,
                                NULLIF(%(Prerequisite)s, '')
                            )
                            ON CONFLICT DO NOTHING;
                            """,
                            {
                                "Department": row['course_department'],
                                "Level": row['course_level'] if row['course_level'] and not row['course_level'].isspace() else None,
                                "Prerequisite": prereq
                            }
                        )
                    # populate coereqs table, must come after course population b/c ref integrity
                    coreqs = literal_eval(row['corequisites']) if row['corequisites'] else []
                    for coreq in coreqs:
                        transaction.execute(
                            """
                            INSERT INTO course_corequisite (
                                department,
                                level,
                                corequisite
                            )
                            VALUES (
                                NULLIF(%(Department)s, ''),
                                %(Level)s,
                                NULLIF(%(Corequisite)s, '')
                            )
                            ON CONFLICT DO NOTHING;
                            """,
                            {
                                "Department": row['course_department'],
                                "Level": row['course_level'] if row['course_level'] and not row['course_level'].isspace() else None,
                                "Corequisite": coreq
                            }
                        )
                except Exception as e:
                    print(e)
                    conn.rollback()
                    return (False, e)
        conn.commit()
        return (True, None)


if __name__ == "__main__":
    # os.chdir(os.path.abspath("../rpi_data"))
    # fileNames = glob.glob("*.csv")
    csv_text = open('../../../rpi_data/fall-2020.csv', 'r')
    courses = Courses(connection.db)
    courses.populate_from_csv(csv_text)
