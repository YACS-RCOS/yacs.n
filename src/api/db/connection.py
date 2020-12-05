import psycopg2
import psycopg2.extras
import os

from constants import Constants

class database():
    def connect(self):
        self.conn = psycopg2.connect(
            dbname=Constants.DB_NAME,
            user=Constants.DB_USER,
            password=Constants.DB_PASS,
            host=Constants.DB_HOST,
            port=Constants.DB_PORT,
        )
        print("[INFO] Database Connected")

    def close(self):
        self.conn.close()

    def execute(self, sql, args, isSELECT=True):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret = None
        try:
            if isSELECT:
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


db = database()
db.connect()
