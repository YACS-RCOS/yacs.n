from datetime import date
class MajorTemplates:
    def __init__(self, db_conn):
        self.db_conn = db_conn
    '''
    Input:
        major: student's major
        year: Which year in templates{'First Year','Second Year','Third Year','Fourth Year'}
        semester: {'Summer', 'Fall', 'Spring'}
    Output:
        the offcial template of the given major, year ,and semester.
    '''
    def find_major_template(self, major, year, semester):
        sql =   """
                SELECT * 
                FROM public."majorTemplates" 
                WHERE
                "Major" = %s
                and "Year" = %s
                and "Semester" = %s
                ORDER BY 
                "Major" ASC,
                array_position(array['First Year','Second Year','Third Year','Fourth Year'], "Year") ASC,
                array_position(array['Summer', 'Fall', 'Spring'], "Semester") ASC;
                """
        args = (str(major), str(year), str(semester))
        return self.db.execute(sql, args, True)
    '''
    Input:
        major: student's major
        year: Which year in templates{'First Year','Second Year','Third Year','Fourth Year'}
        semester: {'Summer', 'Fall', 'Spring'}
    Output:
        The list of courses in the offcial template of the given major, year ,and semester.
    '''
    def find_courses(self, major, year, semester):
        sql =   """
                SELECT unnest("Courses")
                FROM public."majorTemplates" 
                WHERE
                "Major" = %s
                and "Year" = %s
                and "Semester" = %s;
                """
        args = (str(major), str(year), str(semester))
        return self.db.execute(sql, args, True)
    '''
    Input:
        major: student's major
        year: program start year
        semester: {'Summer', 'Fall', 'Spring'}
    Output:
        The list of courses a student should already taken.
    '''
    def find_courses_already_taken(self, major, year, semester):
        todays_date = date.today()
        current_year = int(todays_date.year) - int(year)
        current_term = "First Year"
        if current_year == 0:
            current_term = "First Year"
        elif current_year == 1 and semester == "Spring":
            current_term = "First Year"
        elif current_year == 1 and semester == "Fall":
            current_year = "Second Year"
        elif current_year == 2 and semester == "Spring":
            current_term = "Second Year"
        elif current_year == 2 and (semester == "Fall" or semester == "Summer"):
            current_term = "Third Year"
        elif current_year == 3 and (semester == "Spring" or semester == "Summer"):
            current_term = "Third Year"
        elif current_year == 3 and semester == "Fall":
            current_year = "Fourth Year"
        elif current_year == 4 and semester == "Spring":
            current_term = "Fourth Year"
        else:
            current_term = "Fifth Year"


        sql =   """
                SELECT unnest("Courses")
                FROM public."majorTemplates" 
                WHERE
                array_position(array['First Year','Second Year','Third Year','Fourth Year'], "Year") < array_position(array['First Year','Second Year','Third Year','Fourth Year'], %s)
                and "Major" = %s
                UNION
                SELECT unnest("Courses")
                FROM public."majorTemplates" 
                WHERE
                array_position(array['First Year','Second Year','Third Year','Fourth Year'], "Year") = array_position(array['First Year','Second Year','Third Year','Fourth Year'], %s)
                and "Major" = %s
                and array_position(array['Spring','Summer','Fall'], "Semester") <= array_position(array['Spring','Summer','Fall'], %s)
                """
        args = (str(current_term), str(major), str(current_term), str(major), str(semester))
        return self.db.execute(sql, args, True)