from db.model import Model

class UserEvent(Model):
    def add_event(self, uid, event_id, data, timestamp):
        sql = """INSERT INTO public.userevents ("eventID", "uid", "data", "createdAt")
                 VALUES (%s, %s, %s, %s)"""
        args = (event_id, uid, data, timestamp)
        return self.db.execute(sql, args, False)[0]
