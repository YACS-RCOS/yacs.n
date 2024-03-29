"""
Module for managing final exams
"""
import asyncio
from psycopg2.extras import RealDictCursor

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection

class Finals:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def add_final(self, data):
        """
        Adds a final to the database, with its data being stored in a dict in the data parameter.
        Any values not present in the data dict are automatically added with None as theit value.
        Returns a boolean and string, the bool indicates whether the operation was a success
        and the string is the error, if it is not successful.
        The following values can be present in the dict:
        crn: the crn, must be present
        department: the 4-letter department code
        level: the course level number
        section: the section
        title: the title
        full_title: the full title
        location: the location
        day: the day the final takes place on: M, T, W, R, F.
        start_time: start time
        end_time: the end time
        """
        for i in ("crn", "department", "level", "section", "title", "full_title", "location",
                  "day", "start_time", "end_time"):
            if i not in data:
                data[i] = None
        if data["crn"] is None:
            return False, "CRN cannot be null"
        self.db_conn.execute("""
                            INSERT INTO finals(
                                CRN,
                                Department,
                                Level,
                                Section,
                                Title,
                                Full_title,
                                Location,
                                Day,
                                Start_time,
                                End_time
                            ) VALUES (
                                %(crn)s,
                                NULLIF(%(department)s, ''),
                                NULLIF(%(level)s, ''),
                                NULLIF(%(section)s, ''),
                                NULLIF(%(title)s, ''),
                                NULLIF(%(full_title)s, ''),
                                NULLIF(%(location)s, ''),
                                NULLIF(%(day)s, ''),
                                NULLIF(%(start_time)s, ''),
                                NULLIF(%(end_time)s, ''),
                            )
                            ON CONFLICT DO NOTHING;
                            """, data, False)
        return True, ""

    def populate_from_json(self, json_data):
        """
        Populates the finals table in the same way as add_final
        """
        conn = self.db_conn.get_connection()

        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                # Iterate over each entry in the JSON data
                for entry in json_data:
                    for i in ("crn", "department", "level", "section", "title", "full_title",
                              "location", "day", "start_time", "end_time"):
                        if i not in entry:
                            entry[i] = None
                    try:
                        transaction.execute("""
                                            INSERT INTO finals(
                                                CRN,
                                                Department,
                                                Level,
                                                Section,
                                                Title,
                                                Full_title,
                                                Location,
                                                Day,
                                                Start_time,
                                                End_time
                                            ) VALUES (
                                                %(crn)s,
                                                NULLIF(%(department)s, ''),
                                                NULLIF(%(level)s, ''),
                                                NULLIF(%(section)s, ''),
                                                NULLIF(%(title)s, ''),
                                                NULLIF(%(full_title)s, ''),
                                                NULLIF(%(location)s, ''),
                                                NULLIF(%(day)s, ''),
                                                NULLIF(%(start_time)s, ''),
                                                NULLIF(%(end_time)s, ''),
                                            )
                                            ON CONFLICT DO NOTHING;
                                            """, entry)
                    except Exception as e:
                        # Roll back the transaction and return the exception if an error occurs
                        print("THIS IS THE EXCEPTION: ", e)
                        conn.rollback()
                        return (False, e)
            except ValueError as ve:
                # Return an error message if the JSON data is invalid
                return (False, f"Invalid JSON data: {str(ve)}")

            # Commit the transaction if all entries are inserted successfully
            conn.commit()

            return (True, None)

    def remove_final(self, crn, section=None):
        """
        Removes the final that matches the crn (and if provided, the section) from the table
        On error, returns the error
        """
        if section is None:
            return self.db_conn.execute("""
                                        DELETE FROM finals
                                        WHERE crn = '%(crn)s'
                                        """, {"crn": crn}, False)

        return self.db_conn.execute("""
                                    DELETE FROM finals
                                    WHERE crn = '%(crn)s' AND section = '%(day)s'
                                    """,
                                    {
                                        "crn": crn,
                                        "section": section
                                    }, False)
