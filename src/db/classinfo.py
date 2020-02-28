class ClassInfo:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.interface_name = 'class-info'

    def get_classes(self):
        return self.db_conn.execute("""
            select
                department,
                level,
                max(title) as title,
                json_agg(crn) as crns
            from
                course
            group by
                department,
                level
        """, None, True)

    def get_departments(self):
        return self.db_conn.execute("""
            select
                distinct(department)
            from
                course
        """, None, True)

# c = get_classes()
# print(c[0].class)
# print(c[0].title)
# print(get_classes())
