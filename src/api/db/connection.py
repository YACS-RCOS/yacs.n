import os
import psycopg2
import psycopg2.extras

# connection details
DB_NAME = os.environ.get('DB_NAME', 'yacs')
DB_USER = os.environ.get('DB_USER', None)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', None)
DB_PASS = os.environ.get('DB_PASS', None)

class Database():
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
        )
        print("[INFO] Database Connected")

    def close(self):
        self.conn.close()

    def execute(self, sql, args, is_select=True):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret = None
        try:
            if is_select:
                cur.execute(sql, args)
                ret = cur.fetchall()
            else:
                cur.execute(sql, args)
                ret = 0
                self.conn.commit()

        except psycopg2.Error as e:
            print("DATABASE ERROR: ", end="")
            print(e)
            self.conn.rollback()
            return (ret, e)

        return (ret, None)

    def get_connection(self):
        return self.conn


db = Database()
db.connect()
