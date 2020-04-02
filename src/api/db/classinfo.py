class ClassInfo:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.interface_name = 'class-info'

    def get_classes(self):
        return self.db_conn.execute("""
            select
                department,
                level,
                concat(course.department, '-', course.level) as name,
                max(title) as title,
                json_agg(crn) as crns,
                semester
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
              concat(c.department, '-', c.level) as name,
              max(c.title) as title,
              c.date_start,
              c.date_end,
              json_agg(
                row_to_json(section.*)
              ) sections,
              c.semester
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
              c.level = section.level and
              c.crn = section.crn
            group by
              c.department,
              c.level,
              c.date_start,
              c.date_end,
              c.semester
            order by
              c.department asc,
              c.level asc
        """, None, True)

    def get_departments(self):
        return self.db_conn.execute("""
            select
                distinct(department)
            from
                course
            order by
                department asc
        """, None, True)

    def get_subsemesters(self):
        return self.db_conn.execute("""
            select
              c.date_start,
              c.date_end,
              (SELECT semester_part_name FROM semester_date_range sdr WHERE sdr.date_start = c.date_start AND sdr.date_end = c.date_end),
              c.semester AS parent_semester_name
            from
              course c
            group by
              c.date_start,
              c.date_end,
              c.semester
            order by
              c.date_start asc,
              c.date_end desc
        """, None, True)

    def get_semesters(self):
        return self.db_conn.execute("""
            select
              semester
            from
              course
            group by
              semester
        """, None, True)
        
