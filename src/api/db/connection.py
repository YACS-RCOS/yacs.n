from tortoise import Tortoise
import os

# connection details
DB_NAME = os.environ.get('DB_NAME', 'yacs')
DB_USER = os.environ.get('DB_USER', None)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', None)
DB_PASS = os.environ.get('DB_PASS', None)

class database():
    async def connect(self):
        await Tortoise.init(
            {
                "connections": {
                    "default": {
                        "engine": "tortoise.backends.asyncpg",
                        "credentials": {
                            "host": DB_HOST,
                            "port": DB_PORT,
                            "user": DB_USER,
                            "password": DB_PASS,
                            "database": DB_NAME,
                        },
                    }
                },
                "apps": {"models": {"models": ["models"], "default_connection": "default"}},
            },
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
