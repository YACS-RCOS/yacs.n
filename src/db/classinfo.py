class ClassInfo:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.interface_name = 'class-info'

    def get_classes(self):
        return self.db_conn.execute("""
            select
                department,
                level,
                concat(department, '-', level) as name,
                max(title) as title,
                json_agg(crn) as crns
            from
                course
            group by
                department,
                level
        """, None, True)

    def get_classes_full(self):
        return self.db_conn.execute("""
            select
              c.department,
              c.level,
              max(c.title) as title,
              json_agg(
                row_to_json(section.*)
              ) sections
            from
              course c
            left join
            (
              select
                c1.crn,
                c1.semester,
                max(c1.department) as department,
                max(c1.level) as level,
                json_agg(
                  row_to_json(cs.*)
                ) sessions
              from
                course c1
              join course_session cs on
                c1.crn = cs.crn and
                c1.semester = cs.semester
              group by
                c1.crn,
                c1.semester
            ) section
            on
              c.department = section.department and
              c.level = section.level
            group by
              c.department,
              c.level
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
