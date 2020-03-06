import psycopg2
import psycopg2.extras
import os

# connection details
DB_NAME = os.environ.get('DB_NAME', 'yacs')
DB_USER = os.environ.get('DB_USER', '')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PASS = os.environ.get('DB_PASS', '')


class database():
    def __init__(self):
        self.connect_str = "dbname='{}' user='{}' host='{}' password='{}'".format(
            DB_NAME, DB_USER, DB_HOST, DB_PASS)

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                self.connect_str)
        except:
            print("Fail to connect to database.")

    def close(self):
        self.conn.close()

    def execute(self, sql, args, isSELECT=True):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            if isSELECT:
                cur.execute(sql, args)
                ret = cur.fetchall()
            else:
                cur.execute(sql, args)
                ret = 0
                self.conn.commit()

        except psycopg2.Error as e:
            print(e)
            return None

        return ret

    def get_connection(self):
        return self.conn

print("dbname='{}' user='{}' host='{}' password='{}'".format(
            DB_NAME, DB_USER, DB_HOST, DB_PASS))
db = database()
db.connect()
