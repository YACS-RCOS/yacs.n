from db.model import *

class UserEvent(Model):
    def __init__(self):
        super().__init__()
        
    def addEvent(self, uid, eventID, data, timestamp):
        sql = """INSERT INTO public.userevents ("eventID", "uid", "data", "createdAt") VALUES (%s, %s, %s, %s)"""
        args = (eventID, uid, data, timestamp)
        return self.db.execute(sql, args, False)[0]
