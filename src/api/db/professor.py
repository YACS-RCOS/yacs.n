class Professor:
    def __init__(self, db_conn):
        self.db_conn = db_conn
    
    def add_professor(self, first_name, last_name, phone, email, dep, office, 
        classes, office_time):
        sql = 	"""
                    INSERT INTO
                        professor (first_name, last_name, phone_numbber, email,
                        department, office_room, classes, office_hours_time)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """
        resp, error = self.db_conn.execute(sql, [first_name, last_name, phone, #find out what resp does
        email, dep, office, classes, office_time], False)
        return (True, None) if not error else (False, error)

    def remove_professor(self, first_name, last_name, phone, email, dep, office, 
        classes, office_time):
        if email is None:
            sql =   """
                    DELETE FROM 
                        professor
                    WHERE
                        email = %s 
                    """
            error = self.db_conn.execute(sql, [first_name, last_name, phone, 
            email, dep, office, classes, office_time], False)
        else:
            sql =   """
                    DELETE FROM 
                        professor
                    WHERE
                        first_name = %s AND 
                        last_name = %s AND 
                        phone_number = %s AND 
                        email = %s AND
                        department = %s AND
                        office_room = %s AND
                        classes = %s AND 
                        office_hours_time = %s
                    """
            error = self.db_conn.execute(sql, [first_name, last_name, phone, 
            email, dep, office, classes, office_time], False)
        return (True, None) if not error else (False, error)

    def get_professor_info_by_email(self,email):
        if email is None:
            sql =   """ 
                        select
                            *
                        from
                            professor
                        where
                            email = %s
                    """
        #add the vriables in semester_info
        info, error = self.db_conn.execute(sql, [email], True)
        return (info, None) if not error else (False, error)


    def get_professor_name_by_email(self,email):
        if email is None:
            sql =   """ 
                        select
                            first_name, 
                            last_name, 
                        from
                            professor
                        where
                            email = %s
                    """
        name, error = self.db_conn.execute(sql, [email], True)
        return (name, None) if not error else (False, error)
        
    
    def get_professor_info_by_rcs(self,rcs):
        return self.get_professor_name_by_email(self, rcs+"rpi.edu")

    #gets classes, name(both first and last --> return json file), phone_nu,.... office horus time
    # return all professrs in a dtabase (json)
    # return all the parofesors in a certain department (json)
    # return all professrs that teach a certain class throughout curretn sesmter (json)
