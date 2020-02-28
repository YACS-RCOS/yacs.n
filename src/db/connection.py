import psycopg2


class database():
    def __init__(self):
        self.connect_str = "dbname='{}' user='{}' host='{}' password='{}'".format(
            "yacs", "", "localhost", "")

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                self.connect_str)
        except:
            print("Fail to connect to database.")

    def close(self):
        self.conn.close()

    def execute(self, sql, args, isSELECT):
        cur = self.conn.cursor()
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
