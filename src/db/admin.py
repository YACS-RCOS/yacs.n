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
			group by
				semester
		""", None, True)

	def set_semester_default(self, semester):
		try:
			cmd = """
				UPDATE 
					admin_settings
				SET
					semester = "%s"
			"""
			self.db_conn.execute(cmd, [semester], True)

		except Exception as e:
			self.db_conn.rollback()
			return (False, e)

		return(True, None)