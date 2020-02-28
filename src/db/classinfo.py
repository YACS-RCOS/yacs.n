class ClassInfo:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.interface_name = 'class-info'

    def get_classes(self):
        return self.db_conn.execute("""
            select
              distinct concat(c.department, '-', c.level) as class,
              cd.title
            from
              (
                select
                  department, level
                from
                  course
                group by
                  department,
                  level
              ) c
            join course cd on
              c.department = cd.department and
              c.level = cd.level;
        """, None, True)

# c = get_classes()
# print(c[0].class)
# print(c[0].title)
# print(get_classes())
