class Admin:
	def __init__(self, db_conn):
		self.db_conn = db_conn
		self.interface_name = 'admin'

	def get_semester_default(self):
		return self.db_conn.execute("""
			select
				semester
			from
				admin_setting
		""", None, True)

	def set_semester_default(self, sem):
		cmd = """
			update
				admin_settings
			set
				semester = %s
		"""
		return self.db_conn.execute(cmd, (sem), True)