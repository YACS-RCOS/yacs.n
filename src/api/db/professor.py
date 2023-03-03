from tkinter import INSERT
from tkinter.tix import InputOnly

class Professor:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.interface_name = 'professor'
    
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
        resp, error = self.db_conn.execute(sql, [first_name, last_name, phone, 
        email, dep, office, classes, office_time], False)
        return (True, None) if not error else (False, error)

    def remove_professor(self,email):
        if email is None:
            return

    #get_professor -> gets all informatio from professor 
    # get_email -> remail
    #gets classes, name(both first and last --> return json file), phone_nu, , office horus time
    #new function array of prfoessors in json
    #functions given professor email, find professor (search inside json)
    # return all professrs in a dtabase (json)
    # return all the parofesors in a certain department (json)
    # return all professrs that teach a certain class throughout curretn sesmter (json)
