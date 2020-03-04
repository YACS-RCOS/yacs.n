import psycopg2
from .. import database


class Model(object):
    def __init__(self):
        self.pg = database.database()
        self.pg.connect()

    def __del__(self):
        self.pg.close()
