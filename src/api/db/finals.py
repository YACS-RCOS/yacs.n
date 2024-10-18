import csv
import re
from psycopg2.extras import RealDictCursor
from ast import literal_eval
import asyncio

# https://stackoverflow.com/questions/54839933/importerror-with-from-import-x-on-simple-python-files
if __name__ == "__main__":
    import connection
else:
    from . import connection


class Finals:
    def __init__(self, db_wrapper):
        self.db = db_wrapper

    def populate_from_csv(self, csv_text):
        conn = self.db.get_connection()
        reader = csv.DictReader(csv_text)
        # for each course entry insert sections and course sessions
        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            for row in reader:
                try:
                    # finals
                    transaction.execute(
                            """
                            INSERT INTO
                                final(
                                    semester,
                                    course,
                                    section,
                                    "start",
                                    "end",
                                    room_assignment
                                )
                            VALUES (
                                %(Semester)s,
                                %(Course)s,
                                %(Section)s,
                                TO_TIMESTAMP(%(Start)s, 'YYYY-MM-DD HH24:MI:SS'),
                                TO_TIMESTAMP(%(End)s, 'YYYY-MM-DD HH24:MI:SS'),
                                %(Room_Assignment)s
                            )
                            ON CONFLICT (semester, course, section, room_assignment) DO NOTHING;
                            """,
                            {
                                "Semester": row['Season'] + ' ' + row['Year'],
                                "Course": row['Major'] + '-' + row['Course'],
                                "Section": 1 if row['Section'] == '' else row['Section'],
                                "Start": row['Start'],
                                "End": row['End'],
                                "Room_Assignment": row['Building'] + '-' + row['Room_Number']
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
    csv_text = open('../../../rpi_data/out.csv', 'r')
    finals = Finals(connection.db)
    finals.populate_from_csv(csv_text)
