import psycopg2
import psycopg2.extras


class database():
    def __init__(self):
        self.connect_str = "dbname='{}' user='{}' host='{}' password='{}'".format(
            "yacs", "corey", "localhost", "admin")

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                self.connect_str)
        except:
            print("Fail to connect to database.")

    def close(self):
        self.conn.close()

    def execute(self, sql, args, isSELECT):
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


db = database()
db.connect()
