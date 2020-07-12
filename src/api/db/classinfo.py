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

    def get_classes_full(self, semester=None):
        if semester is not None:
          classes_by_semester_query = """
            select
              c.department,
              c.level,
              concat(c.department, '-', c.level) as name,
              max(c.title) as title,
              c.full_title,
              c.description,
              c.frequency,
              (
                SELECT json_agg(copre.prerequisite)
                FROM course_prerequisite copre
                WHERE c.department=copre.department
                  AND c.level=copre.level
              ) AS prerequisites,
              (
                SELECT json_agg(coco.corequisite)
                FROM course_corequisite coco
                WHERE c.department=coco.department
                  AND c.level=coco.level
              ) AS corequisites,
              c.raw_precoreqs,
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
            WHERE
              c.semester = %s
            group by
              c.department,
              c.level,
              c.date_start,
              c.date_end,
              c.semester,
              c.full_title,
              c.description,
              c.frequency,
              c.raw_precoreqs
            order by
              c.department asc,
              c.level asc
          """
          return self.db_conn.execute(classes_by_semester_query, [semester], True)
        all_classes_query = """
            select
              c.department,
              c.level,
              concat(c.department, '-', c.level) as name,
              max(c.title) as title,
              c.full_title,
              c.description,
              c.frequency,
              (
                SELECT json_agg(copre.prerequisite)
                FROM course_prerequisite copre
                WHERE c.department=copre.department
                  AND c.level=copre.level
              ) AS prerequisites,
              (
                SELECT json_agg(coco.corequisite)
                FROM course_corequisite coco
                WHERE c.department=coco.department
                  AND c.level=coco.level
              ) AS corequisites,
              c.raw_precoreqs,
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
              c.semester,
              c.full_title,
              c.description,
              c.frequency,
              c.raw_precoreqs
            order by
              c.department asc,
              c.level asc
        """
        return self.db_conn.execute(all_classes_query, None, True)


    def get_departments(self):
        return self.db_conn.execute("""
            select
                distinct(department)
            from
                course
            order by
                department asc
        """, None, True)

    def get_subsemesters(self, semester=None):
      if semester is not None:
        return self.db_conn.execute("""
            select
              c.date_start,
              c.date_end,
              (SELECT semester_part_name FROM semester_date_range sdr WHERE sdr.date_start = c.date_start AND sdr.date_end = c.date_end),
              c.semester AS parent_semester_name
            from
              course c
            WHERE
              c.semester = %s
            group by
              c.date_start,
              c.date_end,
              c.semester
            order by
              c.date_start asc,
              c.date_end desc
        """, [semester], True)
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

    def get_semesters(self, includeHidden=False):
      if includeHidden:
        return self.db_conn.execute("""
            select
              semester
            from
              semester_info
        """, None, True)
      return self.db_conn.execute("""
          select
            semester
          from
            semester_info
          where
            public = true::boolean
      """, None, True)

    def get_all_semester_info(self):
      return self.db_conn.execute("""
            SELECT
              *
            FROM
              semester_info
            ;
      """, None, True)

    def get_classes_by_search(self, semester=None, search=None):
      if semester is not None:
        # parse search string to a format recognized by to_tsquery
        ts_search = None if search is None else search.strip().replace(' ', '&')
        return self.db_conn.execute("""
            WITH ts AS (
              SELECT
                c.department,
                c.level,
                CONCAT(c.department, '-', c.level) AS name,
                MAX(c.title) AS title,
                c.full_title,
                c.description,
                c.frequency,
                MAX(c.ts_rank) AS ts_rank,
                (
                  SELECT JSON_AGG(copre.prerequisite)
                  FROM course_prerequisite copre
                  WHERE c.department=copre.department
                  AND c.level=copre.level
                ) AS prerequisites,
                (
                  SELECT JSON_AGG(coco.corequisite)
                  FROM course_corequisite coco
                  WHERE c.department=coco.department
                  AND c.level=coco.level
                ) AS corequisites,
                c.raw_precoreqs,
                c.date_start,
                c.date_end,
                JSON_AGG(
                  row_to_json(section.*)
                ) sections,
                c.semester
              FROM
              (
                SELECT 
                  *,
                  ts_rank_cd(course.tsv, to_tsquery(%(search)s)) AS ts_rank
                FROM
                  course
              ) AS c
              LEFT JOIN
              (
              SELECT
                c1.crn,
                c1.semester,
                MAX(c1.department) AS department,
                MAX(c1.level) as level,
                JSON_AGG(
                  row_to_json(cs.*)
                ) sessions
              FROM
                course c1
              JOIN course_session cs on
                c1.crn = cs.crn and
                c1.semester = cs.semester
              GROUP BY
                c1.crn,
                c1.semester
              ) section
              ON
                c.department = section.department and
                c.level = section.level and
                c.crn = section.crn
              WHERE
                c.semester = %(semester)s
                AND c.tsv @@ to_tsquery(%(search)s)
              GROUP BY
                c.department,
                c.level,
                c.date_start,
                c.date_end,
                c.semester,
                c.full_title,
                c.description,
                c.frequency,
                c.raw_precoreqs
              ORDER BY
                ts_rank DESC,
                department ASC,
                level ASC
            )
            SELECT * FROM ts
            UNION ALL
            SELECT *
            FROM
            (
              SELECT
                c.department,
                c.level,
                CONCAT(c.department, '-', c.level) AS name,
                MAX(c.title) AS title,
                c.full_title,
                c.description,
                c.frequency,
                MAX(c.ts_rank) AS ts_rank,
                (
                  SELECT JSON_AGG(copre.prerequisite)
                  FROM course_prerequisite copre
                  WHERE c.department=copre.department
                  AND c.level=copre.level
                ) AS prerequisites,
                (
                  SELECT JSON_AGG(coco.corequisite)
                  FROM course_corequisite coco
                  WHERE c.department=coco.department
                  AND c.level=coco.level
                ) AS corequisites,
                c.raw_precoreqs,
                c.date_start,
                c.date_end,
                JSON_AGG(
                  row_to_json(section.*)
                ) sections,
                c.semester
              FROM
              (
                SELECT 
                  *,
                  ts_rank_cd(course.tsv, to_tsquery(%(search)s)) AS ts_rank
                FROM
                  course
              ) AS c
              LEFT JOIN
              (
              SELECT
                c1.crn,
                c1.semester,
                MAX(c1.department) AS department,
                MAX(c1.level) as level,
                JSON_AGG(
                  row_to_json(cs.*)
                ) sessions
              FROM
                course c1
              JOIN course_session cs on
                c1.crn = cs.crn and
                c1.semester = cs.semester
              GROUP BY
                c1.crn,
                c1.semester
              ) section
              ON
                c.department = section.department and
                c.level = section.level and
                c.crn = section.crn
              WHERE
                c.semester = %(semester)s
                AND c.full_title ILIKE %(searchAny)s
              GROUP BY
                c.department,
                c.level,
                c.date_start,
                c.date_end,
                c.semester,
                c.full_title,
                c.description,
                c.frequency,
                c.raw_precoreqs
              ORDER BY
                ts_rank DESC,
                department ASC,
                level ASC
            ) q2
            WHERE NOT EXISTS (
              SELECT * FROM ts
            )            
        """, {
          'search': ts_search,
          'searchAny': '%' + search + '%',
          'semester': semester
        }, True)
      return None
