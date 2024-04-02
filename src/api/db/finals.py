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

    def populate_from_json(self, json_data):
        """
        Populates the finals table with an array of json data
        Any values not present in a data entry are automatically added with None as theit value.
        Returns a boolean and string, the bool indicates whether the operation was a success
        and the string is the error, if it is not successful.
        The following values can be present in each entry:
        crn: the crn, must be present
        department: the 4-letter department code
        level: the course level number
        section: the section
        title: the title
        full_title: the full title
        location: the location
        day: integer representation of the day the final takes place on: M=0, T=1, W=2, R=3, F=4.
        start_time: start time
        end_time: the end time
        """
        conn = self.db_conn.get_connection()

        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                # Iterate over each entry in the JSON data
                for entry in json_data:
                    for i in ("crn", "department", "level", "section", "title", "full_title",
                              "location", "day", "start_time", "end_time"):
                        if i not in entry:
                            # change behavior here if null data is bad
                            entry[i] = None
                    try:
                        transaction.execute("""
                                            INSERT INTO finals (
                                                crn,
                                                department,
                                                level,
                                                section,
                                                title,
                                                full_title,
                                                location,
                                                day,
                                                start_time,
                                                end_time
                                            ) VALUES (
                                                %(crn)s,
                                                %(department)s,
                                                %(level)s,
                                                %(section)s,
                                                %(title)s,
                                                %(full_title)s,
                                                %(location)s,
                                                %(day)s,
                                                %(start_time)s,
                                                %(end_time)s
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

    def get_finals_data(self):
        """
        Returns a list of CRNs for all classes with finals data. Note that some of the
        data may be null
        """
        finals_data = self.db_conn.execute("""
                                           SELECT crn FROM finals;
                                           """, {}, True)
        ret = []
        for i in finals_data[0]:
            ret.append(i["crn"])
        return ret

    def get_single_final_data(self, crn):
        """
        Returns the finals data for the crn provided.
        """
        return self.db_conn.execute("""SELECT
                                    * FROM finals
                                    WHERE 
                                    crn = %(crn)s""", {"crn": crn}, True)[0][0]

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
