class Professor:
    def __init__(self, db_conn):
        self.db_conn = db_conn
    
    def add_professor(self, first_name, last_name, phone, email, dep, office, 
        classes, office_time, rcs):
        sql = 	"""
                    INSERT INTO
                        professor (first_name, last_name, phone_numbber, email,
                        department, office_room, classes, office_hours_time, rcs)
                    VALUES
                        (%(First_name)s, %(Last_name)s, %(Phone_number)s, %(Email)s, %(Dep)s, %(Office_room)s, %(Classes)s, %(Office_time)s, %(Rcs_id)s),
                    ON CONFLICT DO NOTHING;
                    """
        {
            "First_name": first_name,
            "Last_name": last_name,
            "Phone_number": phone,
            "Email": email,
            "Dep": dep,
            "Office_room": office,
            "Classes": classes, 
            "Office_time": office_time,
            "Rcs_id": rcs
        }, 
        resp, error = self.db_conn.execute(sql, [first_name, last_name, phone, 
        email, dep, office, classes, office_time], False)
        return (True, None) if not error else (False, error)

    def remove_professor_by_email(self, email):
        if email is None:
            sql =   """
                    DELETE FROM 
                        professor
                    WHERE
                        email = %(Email)s 
                    """
            {
                "Email": email
            }
            error = self.db_conn.execute(sql, [email], False)
        else:
            sql =   """
                    DELETE FROM 
                        professor
                    WHERE
                        email = %(Email)s
                    """
            {
                "Email": email
            }
            error = self.db_conn.execute(sql, [email], False)
        return (True, None) if not error else (False, error)

    def get_professor_info_by_email(self,email):
        if email is None:
            sql =   """ 
                        select
                            *
                        from
                            professor
                        where
                            email = %(Email)s
                    """
            {
                "Email": email
            }
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
                            email = %(Email)s
                    """
            {
                "Email": email
            }
        name, error = self.db_conn.execute(sql, [email], True)
        return (name, None) if not error else (False, error)
    
    def get_professor_info_by_rcs(self,rcs):
        return self.get_professor_name_by_email(self, rcs+"rpi.edu")

    #get rcs by email
    #get office hours by email (make speical case for no value)

    #return as a json
    def get_all_professors(self):  
        return self.db_conn.execute("SELECT * FROM professor")
    
    #gets prfoessors' phone number by their email
    def get_prfoessor_phone_number_by_email(self, email):
        if email is None:
            sql =   """ 
                        select
                            phone_number
                        from
                            professor
                        where
                            email = %(Email)s
                    """
            {
                "Email": email
            }
        email, error = self.db_conn.execute(sql, [email], True)
        return (email, None) if not error else (False, error)

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
        {
            "Department": department
        }
        department, error = self.db_conn.execute(sql, None, True)
        return (department, None) if not error else (False, error)

    #gets classes, name(both first and last --> return json file), phone_nu,.... office horus time

