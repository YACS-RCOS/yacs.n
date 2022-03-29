from datetime import datetime
from db.model import *
import uuid


class Session(Model):
    def __init__(self):
        super().__init__()

    def create_session_id(self):
        return str(uuid.uuid1())

    async def start_session(self, session, uid, start_time):
        sql = """INSERT INTO public.user_session (session_id, user_id, start_time) VALUES (%s,%s,%s);"""
        args = (session, uid, start_time)
        return await self.db.execute(sql, args, False)[0]

    async def get_session(self, session_id='%'):
        sql = """   SELECT session_id, user_id, start_time,end_time 
                    FROM public.user_session
                    WHERE   session_id::text LIKE %s"""

        arg = (session_id,)
        return await self.db.execute(sql, arg, True)[0]

    async def end_session(self, session_id='%', uid='%', end_time=datetime.utcnow()):
        sql = """UPDATE public.user_session SET end_time = %s WHERE session_id::text LIKE %s AND user_id::text LIKE %s;"""
        args = (end_time, session_id, str(uid))
        return await self.db.execute(sql, args, False)[0]
