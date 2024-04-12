"""
Module responsible for interacting with the CourseWatchers table, which is used
to send notifications to users when select courses they choose to watch have any
updates of note
"""
import asyncio
from psycopg2.extras import RealDictCursor

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection

class CourseWatchers:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def add_watcher(self, course_crn, user_id):
        """
        Given a course CRN and a user ID, add that user to the list of
        users watching the course
        """
        course_data = self.db_conn.execute("SELECT * FROM course_watch WHERE crn = %(crn)s",
                                           {"crn": "68302"}, True)
        print(course_data)
        self.db_conn.execute("INSERT INTO course_watch (crn, watchers) VALUES (%(crn)s, '{%(watchers)s}') ON CONFLICT DO NOTHING;",
                             {"crn": "68302", "watchers": int(user_id)}, False)
        course_data = self.db_conn.execute("SELECT * FROM course_watch WHERE crn = %(crn)s",
                                           {"crn": "68302"}, True)
        print(course_data)
