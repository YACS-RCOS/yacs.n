from tortoise import Tortoise, run_async
from tortoise.transactions import in_transaction
from tortoise.exceptions import OperationalError
from tortoise.contrib.fastapi import register_tortoise
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
        await Tortoise.generate_schemas(safe=True)

    async def close(self):
        await Tortoise.close_connections()

    async def execute(self, sql, args, isSELECT=True):
        ret = None
        try:
            async with in_transaction() as tconn:
                if isSELECT:
                    ret = await tconn.execute_query_dict(sql % args)
                else:
                    await tconn.execute_query_dict(sql % args)
                    ret = 0

        except OperationalError as e:
            print("DATABASE ERROR: ", end="")
            print(e)
            return (ret, e)

        return (ret, None)

    def get_connection(self):
        return Tortoise.get_connection()

if __name__ == "__main__":
    db = database()
    run_async(db.connect())