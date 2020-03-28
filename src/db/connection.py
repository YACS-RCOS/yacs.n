import psycopg2
import psycopg2.extras
import os

# connection details
DB_NAME = os.environ.get('DB_NAME', 'yacs')
DB_USER = os.environ.get('DB_USER', None)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', None)
DB_PASS = os.environ.get('DB_PASS', None)


class database():
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT,
            )
        except psycopg2.Error as e:
            print(f"Failed to connect to database: {e}")
            print(f"Used {DB_NAME}-{DB_USER}-{DB_HOST}-{DB_PORT}-{DB_PASS}")
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
            return (ret, e)

        return (ret, None)

    def get_connection(self):
        return self.conn


db = database()
db.connect()
