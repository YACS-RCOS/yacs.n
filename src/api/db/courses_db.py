import csv
import json
from psycopg2.extras import RealDictCursor
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


##!!!!!!!!!!!!!!!!!!!!
## TO UPDATE WITH NEW PATHWAYS/CATEGORIES, CHANGE JSON FILE AT BOTTOM OF PAGE
##!!!!!!!!!!!!!!!!!!!!

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection


class HASSCourse:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    def add_course(self, course_name, course_code, dept_code):
        if course_name is not None:
            print(course_name)
            return self.db_conn.execute("""
            INSERT INTO
                courses (course_name, course_code, dept_code)
            VALUES
                   (%(course_name)s, %(course_code)s, %(dept_code)s)
            ON CONFLICT DO NOTHING
            ;
        """, {
                "dept_code": dept_code,
                "course_code": course_code,
                "course_name": course_name,
            }, False)
        else:
            return (False, "course_name cannot be none")

    def add_bulk_courses(self, json_data):  # function is called in app.py
        # Connect to the SQL database
        conn = self.db_conn.get_connection()

        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                # Iterate over each entry in the JSON data
                for entry in json_data:
                    for sub in entry['Pathways']:
                        for key in sub.keys():
                            if key != 'Name' and key != 'Compatible minor(s)':
                                for course in sub[key]:
                                    d_code = ''
                                    c_code = ''
                                    c_name = ''
                                    tokens = course.split('-')
                                    if len(tokens) == 1:
                                        print(tokens[0])
                                        tokens = tokens[0].split()
                                        d_code = tokens[0]
                                        c_code = tokens[1]
                                    else:
                                        dept_and_code = tokens[0].split()
                                        d_code = dept_and_code[0]
                                        c_code = dept_and_code[1]
                                        c_name = tokens[1].strip()
                                    try:
                                        # Insert course name, code, and department into "courses" table (tables/courses.py)
                                        transaction.execute(
                                            """
                                            INSERT INTO courses (
                                                dept_code,
                                                course_code,
                                                course_name
                                            )
                                            VALUES (
                                                NULLIF(%(dept_code)s, ''),
                                                NULLIF(%(course_code)s, ''),
                                                NULLIF(%(course_name)s, '')  
                                            )
                                            ON CONFLICT DO NOTHING;
                                            """,
                                            {
                                                "dept_code": d_code,
                                                "course_code": c_code,
                                                "course_name": c_name
                                            }
                                        )
                                    except Exception as e:
                                        # Roll back the transaction and return the exception if an error occurs
                                        print("THIS IS THE EXCEPTION:", e)
                                        conn.rollback()
                                        return (False, e)
            except ValueError as ve:
                # Return an error message if the JSON data is invalid
                return (False, f"Invalid JSON data: {str(ve)}")

            # Commit the transaction if all entries are inserted successfully
            conn.commit()

            # Invalidate cache to ensure new data is retrieved
            self.clear_cache()

            # Return success status and no error
            return True, None

    def clear_cache(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.cache.clear(namespace="API_CACHE"))
        else:
            asyncio.run(self.cache.clear("API_CACHE"))


if __name__ == "__main__":
    pathways = HASSCourse(connection.db)
    pathways.add_bulk_courses('../../../src/web/src/pages/pathwayV2.json')  # CHANGE FILE HERE IF NEEDED
