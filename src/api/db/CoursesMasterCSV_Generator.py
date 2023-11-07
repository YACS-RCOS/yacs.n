import pandas as pd
import os
import glob
import os
import csv
import re
import json
from psycopg2.extras import RealDictCursor
from ast import literal_eval
import asyncio

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection


################################
class CSV_Generator:
    def __init__(self, db_wrapper, cache):
        self.db = db_wrapper
        self.cache = cache

    def generateCoursesMaster(self, csv_text):
        conn = self.db.get_connection()
        reader = csv.DictReader(csv_text)
        # for each course entry insert sections and course sessions
        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            for row in reader:
                print(row)
                try:
                    # courses
                    transaction.execute(
                        """
                        INSERT INTO
                            course_master(
                                min_credits,
                                max_credits,
                                full_title,
                                department,
                                level,
                                title,
                                raw_precoreqs,
                                school
                            )
                        VALUES (
                            %(min_credits)s,
                            %(max_credits)s,
                            NULLIF(%(full_title)s, ''),
                            %(department)s,
                            %(level)s,
                            NULLIF(%(title)s, ''),
                            NULLIF(%(raw_precoreqs)s, ''),
                            %(school)s
                        )
                        ON CONFLICT DO NOTHING;
                        """,
                        {
                            "min_credits": int(row['course_credit_hours'].split("-")[0]),
                            "max_credits": int(row['course_credit_hours'].split("-")[-1]),
                            "full_title": row["full_name"],  # new
                            "department": row['course_department'],
                            "level": int(row['course_level']) if row['course_level'] and not row[
                                'course_level'].isspace() else None,
                            "title":  row['course_name'],
                            "raw_precoreqs": row['raw_precoreqs'],
                            "school": row['school']
                        }
                    )
                except Exception as e:
                    print(e)
                    conn.rollback()
                    return (False, e)
        conn.commit()
        # invalidate cache so we can get new classes
        # self.clear_cache()
        return (True, None)
    #
    # def clear_cache(self):
    #     try:
    #         loop = asyncio.get_running_loop()
    #     except RuntimeError:
    #         loop = None
    #
    #     if loop and loop.is_running():
    #         loop.create_task(self.cache.clear(namespace="API_CACHE"))
    #     else:
    #         asyncio.run(self.cache.clear("API_CACHE"))

# if __name__ == "__main__":
#     # os.chdir(os.path.abspath("../rpi_data"))
#     # fileNames = glob.glob("*.csv")
#     csv_text = open('../../../rpi_data/fall-2020.csv', 'r')
#     courses = CSV_Generator(connection.db)
#     courses.populate_from_csv(csv_text)
