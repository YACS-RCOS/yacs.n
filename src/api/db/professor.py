class Professor:
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache
    
    def add_professor(self, first_name, last_name, phone, email, dep, office, 
        classes, office_time, rcs):
        if email is not None:
            sql = 	"""
                        INSERT INTO
                            professor (first_name, last_name, phone_number, email,
                            department, office_room, classes, office_hours_time, rcs)
                        VALUES
                            (%(First_name)s, %(Last_name)s, %(Phone_number)s, %(Email)s,
                            %(Dep)s, %(Office_room)s, %(Classes)s, %(Office_time)s, %(Rcs_id)s)
                        ON CONFLICT DO NOTHING;
                    """
            params = {
                "First_name": first_name,
                "Last_name": last_name,
                "Phone_number": phone,
                "Email": email,
                "Dep": dep,
                "Office_room": office,
                "Classes": classes, 
                "Office_time": office_time,
                "Rcs_id": rcs
            }
        resp, error = self.db_conn.execute(sql, params, False)
        return (True, None) if not error else (False, error)

    def remove_professor_by_email(self, email):
        if email is not None:
            sql =   """
                    DELETE FROM 
                        professor
                    WHERE
                        email = %(Email)s 
                    """
            params = {
                "Email": email
            }
            error = self.db_conn.execute(sql, params, False)
        else:
            return (False, "email cant be none")
        return (True, None) 

    # if you expect the SQL statement to return more than one row of data, you should pass True as the value for multi.
    def get_professor_info_by_email(self,email):
        if email is not None:
            sql =   """ 
                        select
                            *
                        from
                            professor
                        where
                            email = %(Email)s
                    """
            params = {
                "Email": email
            }
        info, error = self.db_conn.execute(sql, params, True)
        return (info, None) if not error else (False, error)

    def get_professor_name_by_email(self,email):
        if email is not None:
            sql =   """ 
                        select
                            first_name, 
                            last_name, 
                        from
                            professor
                        where
                            email = %(Email)s
                    """
            params = {
                "Email": email
            }
        name, error = self.db_conn.execute(sql, params, True)
        return (name, None) if not error else (False, error)
    
    def get_professor_info_by_rcs(self,rcs):
        return self.get_professor_info_by_email(rcs+"@rpi.edu")

    def get_professor_rcs_by_email(self,email):
        if email is not None:
            sql =   """
                        select
                            rcs
                        from 
                            professor
                        where 
                            email = %(Email)s
                    """
            params = {
                "Email": email
            }
        rcs, error = self.db_conn.execute(sql , params, True)
        return rcs(None) if not error else(False, error)

    def get_office_hours_by_email(self,email):
        if email is not None:
            sql =   """
                        select 
                            office_room
                            office_hours_time
                        from 
                            professor
                        where 
                            email = %(Email)s
                    """
            params = {
                "Email": email
            }
        office_hours, error = self.db_conn.execute(sql, params, True)
        return (office_hours,error) if not error else (False,error)

    #return as a json
    def get_all_professors(self):  
        return self.db_conn.execute(""" 
                            SELECT * FROM professor
                    """, None, True)
    
    #gets prfoessors' phone number by their email
    def get_professor_phone_number_by_email(self, email):
        if email is not None:
            sql = """ 
                    select
                        phone_number
                    from
                        professor
                    where
                        email = %(Email)s
                    """
            params = {
                "Email": email
            }
            phone_number, error = self.db_conn.execute(sql, params, True)
            return (phone_number, None) if not error else (False, error)


    #seraches professors who are in a certain department
    def get_professors_by_department(self,department): 
        sql =   """
                    select
                        * 
                    from
                        professor
                    where
                        department = %(Department)s
                """
        params = {
            "Department": department
        }
        department, error = self.db_conn.execute(sql, params, True)
        return (department, None) if not error else (False, error)
