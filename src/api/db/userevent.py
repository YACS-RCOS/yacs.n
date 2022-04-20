from db.model import *

class UserEvent(Model):

    def __init__(self):
        super().__init__()
        
    async def addEvent(self, uid, eventID, data, timestamp):
        sql = """INSERT INTO public.user_event (event_id, user_id, content,created_at) VALUES ('%s', '%s', '%s', '%s');"""
        args = (eventID, uid, data, timestamp)
        
        userEvent = await self.db.execute(sql, args, False)
        return userEvent[0]

    async def updateEvent(self, uid, eventID, data):
        sql = """INSERT INTO public.user_event (event_id, user_id, content,created_at) VALUES ('%s', '%s', '%s', '%s');"""
        sql = """   UPDATE
                        public.user_event
                    SET
                        content = '%s'
                    WHERE
                        user_id = '%s' AND event_id = '%s';
                    """
        args = (data,uid,eventID)
        
        userEvent = await self.db.execute(sql, args, False)
        return userEvent[0]