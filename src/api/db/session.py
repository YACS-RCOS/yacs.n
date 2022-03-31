from datetime import datetime
from db.model import *
from models import UserSession
import uuid


class Session(Model):
    def __init__(self):
        super().__init__()

    def create_session_id(self):
        return str(uuid.uuid1())

    async def start_session(self, session, uid, start_time):
        sql = """INSERT INTO public.user_session (session_id, user_id, start_time) VALUES ('%s','%s','%s');"""
        args = (session, uid, start_time)
        # return await UserSession.create(session_id=uuid.UUID(session).hex, user_id=uid, start_time=start_time)
        sess = await self.db.execute(sql, args, False)
        return sess[0]

    async def get_session(self, session_id='%'):
        sql = """   SELECT session_id, user_id, start_time,end_time
                    FROM public.user_session
                    WHERE   session_id::text LIKE '%s'"""

        arg = (session_id,)
        # if session_id is not None:
        #     session_id = uuid.UUID(session_id).hex
        # return await UserSession.get(session_id=session_id).values()
        sess = await self.db.execute(sql, arg, True)
        return sess[0]

    async def end_session(self, session_id='%', uid='%', end_time=datetime.utcnow()):
        sql = """UPDATE public.user_session SET end_time = '%s' WHERE session_id::text LIKE '%s' AND user_id::text LIKE '%s';"""
        args = (end_time, session_id, str(uid))
        sess = await self.db.execute(sql, args, False)
        return sess[0]
        # if session_id is not None:
        #     session_id = uuid.UUID(session_id).hex
        # return await UserSession.filter(session_id=session_id, user_id=uid).update(end_time=end_time)
