class MajorTemplates:
    def __init__(self, db_conn):
        self.db_conn = db_conn
    
    def find_major_template(self, major, year):
        sql =   '''
                SELECT * 
                FROM public."majorTemplates" 
                WHERE
                "Major" = %s
                and "Year" = %s
                ORDER BY 
                "Major" ASC,
                array_position(array['First Year','Second Year','Third Year','Fourth Year'], "Year") ASC,
                array_position(array['Spring','Summer','Fall'], "Semester") ASC;
                '''
        args = (str(major), str(year))
        return self.db.execute(sql, args, True)
    
    def find_courses(self, major, year):
        sql =   '''
                SELECT unnest("Courses")
                FROM public."majorTemplates" 
                WHERE
                "Major" = %s
                and "Year" = %s
                ORDER BY 
                "Major" ASC,
                array_position(array['First Year','Second Year','Third Year','Fourth Year'], "Year") ASC,
                array_position(array['Spring','Summer','Fall'], "Semester") ASC;
                '''
        args = (str(major), str(year))
        return self.db.execute(sql, args, True)

    def find_courses_already_taken(self, major, year, current_courses):
        sql =   '''
                SELECT unnest("Courses")
                FROM public."majorTemplates" 
                WHERE
                array_position(array['First Year','Second Year','Third Year','Fourth Year'], "Year") < array_position(array['First Year','Second Year','Third Year','Fourth Year'], %s)
                and "Major" = %s
                ORDER BY 
                "Major" ASC,
                array_position(array['First Year','Second Year','Third Year','Fourth Year'], "Year") ASC,
                array_position(array['Spring','Summer','Fall'], "Semester") ASC;
                '''
        args = (str(major), str(year))
        return self.db.execute(sql, args, True)
