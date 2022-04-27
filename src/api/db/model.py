import db.connection as connection


class Model(object):
    def __init__(self):
        self.db = connection.database()
