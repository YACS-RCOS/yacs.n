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
    def __init__(self, db_wrapper, cache):
        self.db = db_wrapper
        self.cache = cache

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
                            ON CONFLICT (semester, course, section, start, room_assignment) DO NOTHING;
                            """,
                            {
                                "Semester": row['Season'] + ' ' + row['Year'],
                                "Course": row['Major'] + '-' + row['Course'],
                                "Section": "1" if row['Section'] == '' else row['Section'],
                                "Start": row['Start'],
                                "End": row['End'],
                                "Room_Assignment": row['Building'] + '-' + row['Room_Number']
                            }
                        )
                except Exception as e:
                    print(e)
                    conn.rollback()
                    return e
        conn.commit()
        self.clear_cache()
        return None

    def get_by_semester(self, semester):
        return self.db.execute("""
            SELECT * FROM final
            WHERE semester=%(Semester)s
            ORDER BY start ASC;
        """, {
            "Semester": semester
        }, isSELECT=True)

    def delete_by_semester(self, semester):
        self.clear_cache()
        return self.db.execute("""
            BEGIN TRANSACTION;
                DELETE FROM final
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
        self.clear_cache()
        return None

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
    # os.chdir(os.path.abspath("../rpi_data"))
    # fileNames = glob.glob("*.csv")
    csv_text = open('../../../rpi_data/out.csv', 'r')
    finals = Finals(connection.db)
    finals.populate_from_csv(csv_text)
