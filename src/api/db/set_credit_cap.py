class SetCreditCap:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.interface_name = 'credit_cap'
        
    def set_credit_cap(self, credit_cap, warning_message):
        try:
            delete = "DELETE FROM credit_cap;"
            response, error = self.db_conn.execute(delete, None, isSELECT=False)
        except Exception as e:
            return (False, e)
        if response is None:
            return (False, error)

        try:
            cmd = """
				INSERT INTO credit_cap(cap, credit_cap_warning)
				VALUES(%s, %s)
			"""
            response, error = self.db_conn.execute(cmd, [credit_cap, warning_message], False)
        except Exception as e:
            return (False, e)
		
        if response is not None:
            return (True, None)
        return (False, error)

    def get_credit_cap(self):
        cmd = """
            SELECT cap,credit_cap_warning FROM credit_cap
            LIMIT 1;
        """
        result, error = self.db_conn.execute(cmd,None,True)
        if error:
            return (None,error)
        return (result[0],error)