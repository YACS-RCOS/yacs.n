from db import connection


class Model():
    def __init__(self):
        self.db = connection.db
