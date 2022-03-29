from db.model import *
from models.user_account import UserAccount


class User(Model):
    def __init__(self):
        super().__init__()

    async def get_user(self, args):
        user = await UserAccount.filter(**args).values()
        return user

    async def add_user(self, args):
        added_user = await UserAccount.create(**args)
        return added_user

    async def delete_user(self, uid):
        sql = """DELETE FROM student_course_selection WHERE user_id=%s;
                 DELETE FROM public.user_account WHERE user_id = %s;"""
        args = (uid,uid)
        deleted_user = await self.db.execute(sql, args, False)
        return deleted_user[0]

    async def update_user(self, args):
        sql = """   UPDATE
                        public.user_account
                    SET
                        name        = %(Name)s,
                        email       = %(Email)s,
                        phone       = %(Phone)s,
                        password    = %(Password)s,
                        major       = %(Major)s,
                        degree      = %(Degree)s
                    WHERE
                        user_id = %(UID)s;
                    """
        updated_user = await self.db.execute(sql, args, False)
        return updated_user[0]
