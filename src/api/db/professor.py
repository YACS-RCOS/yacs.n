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

    def get_professor(self, email):
        if email is None:
            sql =   """
                        select
                            varaible name
                    """ 

    #gets classes, name(both first and last --> return json file), phone_nu,.... office horus time
    #new function array of prfoessors in json
    #functions given professor email, find professor (search inside json) i think its done already
    # return all professrs in a dtabase (json)
    # return all the parofesors in a certain department (json)
    #get_professor_name_by_rcsID WHERE p.rcsID =  %s DO
    #get_professor_email_by_name DO
    # return all professrs that teach a certain class throughout curretn sesmter (json)
