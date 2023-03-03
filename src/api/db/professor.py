from tkinter import INSERT
from tkinter.tix import InputOnly

class Professor:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.interface_name = 'professor'
    
    def add_professor(self, first_name, last_name, phone, email, dep, office, 
        classes, office_time, webex):
        sql = 	"""
                    INSERT INTO
                        professor (first_name, last_name, phone_numbber, email,
                        department, office_room, classes, office_hours_time, webex)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """
        resp, error = self.db_conn.execute(sql, [first_name, last_name, phone, 
        email, dep, office, classes, office_time, webex], False)
        return (True, None) if not error else (False, error)

    def remove_professor(self,cid):
        if cid is None:

    #define primary key