from db.model import *
from models.user_account import UserAccount


class User(Model):
    def __init__(self):
        super().__init__()

    async def get_user(self, uid='%', name='%', email='%', password='%', phone='%', major='%', degree='%', enable=True):
        sql = """   SELECT user_id, name, email, phone, password, major, degree, enable, admin, super_admin
                    FROM public.user_account
                    WHERE   user_id::text   LIKE '%s' AND
                            name        LIKE '%s' AND
                            email       LIKE '%s' AND
                            phone       LIKE '%s' AND
                            password    LIKE '%s' AND
                            major       LIKE '%s' AND
                            degree      LIKE '%s' AND
                            enable = '%s'"""

        args = (str(uid), name, email, phone, password, major, degree, enable)
        user = await self.db.execute(sql, args, True)
        return user[0]

    async def add_user(self, args):
        sql = """
                INSERT INTO
                    user_account (
                        name,
                        email,
                        phone,
                        password,
                        major,
                        degree,
                        enable
                    )
                VALUES (
                    '%(Name)s',
                    '%(Email)s',
                    '%(Phone)s',
                    '%(Password)s',
                    '%(Major)s',
                    '%(Degree)s',
                    '%(Enable)s'
                )
                """
        added_user = await self.db.execute(sql, args, False)
        return added_user[0]

    async def delete_user(self, uid):
        selection_sql = """DELETE FROM student_course_selection WHERE user_id='%s';"""
        user_sql = """DELETE FROM user_account WHERE user_id = '%s';"""
        args = (uid,)
        await self.db.execute(selection_sql, args, False)
        deleted_user = await self.db.execute(user_sql, args, False)
        return deleted_user[0]

    async def update_user(self, args):
        sql = """   UPDATE
                        user_account
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
