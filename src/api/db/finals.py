import asyncio

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
        The following values should be present in the dict:
        crn: the crn
        department: the 4-letter department code
        level: the course level number
        section: the section
        title: the title
        full_title: the full title
        location: the location
        day: the day the final takes place on, should be M, T, W, R, F depending on day
        start_time: start time
        end_time: end time
        """
        #TODO: value checking
        self.db_conn.execute("""
                            INSERT INTO finals(
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
                                NULLIF(%(crn)s, ''),
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
