class Admin:
	def __init__(self, db_conn):
		self.db_conn = db_conn
		self.interface_name = 'admin'

	def get_semester_default(self):
		return self.db_conn.execute("""
			select
				semester
			from
				admin_settings
		""", None, True)

	def set_semester_default(self, semester):
		cmd = """
			UPDATE 
				admin_settings
			SET
				semester = "SUMMER 2020"
		"""
		self.db_conn.execute(cmd, None, True)
		return (True, None)