import json

from db.model import *

class User(Model):
    def __init__(self):
        super().__init__()

    def get_user(self, uid='%', name='%', email='%', password='%', phone='%', major='%', degree='%', enable=True):
        sql = """   SELECT user_id, name, email, phone,password,major,degree,enable,admin,super_admin
                    FROM public.user_account
                    WHERE   user_id::text   LIKE %s AND
                            name        LIKE %s AND
                            email       LIKE %s AND
                            phone       LIKE %s AND
                            password    LIKE %s AND
                            major       LIKE %s AND
                            degree      LIKE %s AND
                            enable = %s"""

        args = (str(uid), name, email, phone, password, major, degree, enable)
        result = self.db.execute(sql, args, True)[0]
        if len(result) >= 1 and 'major' in result[0]:
            result[0]['major'] = json.loads(result[0]['major'])
        return result

    def add_user(self, args):
        sql = """
                INSERT INTO
                    public.user_account (
                        name,
                        email,
                        phone,
                        password,
                        major,
                        degree,
                        enable
                    )
                VALUES (
                    %(Name)s,
                    %(Email)s,
                    %(Phone)s,
                    %(Password)s,
                    %(Major)s,
                    %(Degree)s,
                    %(Enable)s
                )
                """
        args['Major'] = json.dumps(args['Major'])
        return self.db.execute(sql, args, False)[0]

    def delete_user(self, uid):
        sql = """DELETE FROM student_course_selection WHERE user_id=%s;
                 DELETE FROM public.user_account WHERE user_id = %s;"""
        args = (uid,uid)
        return self.db.execute(sql, args, False)[0]

    def update_user(self, args):
        sql = """   UPDATE
                        public.user_account
                    SET
                        name        = %(Name)s,
                        email       = %(Email)s,
                        phone       = %(Phone)s,
                        password    = %(NewPassword)s,
                        major       = %(Major)s,
                        degree      = %(Degree)s
                    WHERE
                        user_id = %(UID)s AND
                        password = %(Password)s;
                    """
        args['Major'] = json.dumps(args['Major'])
        return self.db.execute(sql, args, False)[0]