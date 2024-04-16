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
        users watching the course. If the user is already in that list,
        do nothing. If there is not an entry of watchers for the course
        CRN, then add it
        """
        course_data = self.db_conn.execute("SELECT * FROM course_watch WHERE crn = %(crn)s",
                                           {"crn": course_crn}, True)
        if len(course_data[0]) == 0:
            self.db_conn.execute("""INSERT INTO course_watch
                                        (crn, watchers)
                                    VALUES
                                        (%(crn)s, '{%(watchers)s}')
                                    ON CONFLICT DO NOTHING;""",
                                    {"crn": course_crn, "watchers": int(user_id)}, False)
            return
        watcher_list = course_data[0][0]["watchers"].copy()
        print(watcher_list)
        if user_id not in watcher_list:
            watcher_list.append(user_id)
            self.db_conn.execute("""UPDATE course_watch
                                    SET
                                        watchers = %(watchers)s
                                    WHERE
                                        crn = %(crn)s;""",
                                    {"crn": course_crn, "watchers": watcher_list}, False)
        course_data = self.db_conn.execute("SELECT * FROM course_watch WHERE crn = %(crn)s",
                                           {"crn": course_crn}, True)
        print(course_data)

    def remove_watcher(self, course_crn, user_id):
        """
        Given a course crn and user id, remove a user from the list
        of users watching the course. If the operation results in an
        empty list of watchers, leave the empty list in the table.
        """
        course_data = self.db_conn.execute("SELECT * FROM course_watch WHERE crn = %(crn)s",
                                           {"crn": course_crn}, True)
        watcher_list = course_data[0][0]["watchers"].copy()
        print(watcher_list)
        if user_id in watcher_list:
            watcher_list.remove(user_id)
            self.db_conn.execute("""UPDATE course_watch
                                    SET
                                        watchers = %(watchers)s
                                    WHERE
                                        crn = %(crn)s;""",
                                    {"crn": course_crn, "watchers": watcher_list}, False)
        course_data = self.db_conn.execute("SELECT * FROM course_watch WHERE crn = %(crn)s",
                                           {"crn": course_crn}, True)
        print(course_data)

    def get_course_watchers(self, course_crn):
        course_data = self.db_conn.execute("SELECT * FROM course_watch WHERE crn = %(crn)s",
                                           {"crn": course_crn}, True)
        return course_data[0][0]["watchers"]

    def purge_course_watchlist(self):
        """
        Completely wipe the course watch table. Should be called
        if crns change between semesters
        """
        self.db_conn.execute("DELETE FROM course_watch", {}, False)
