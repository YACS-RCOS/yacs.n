class Admin:
	def __init__(self, db_conn):
		self.db_conn = db_conn
		self.interface_name = 'admin_info'

	def get_semester_default(self):
		# NOTE: COALESCE takes first non-null vaue from the list
		result, error = self.db_conn.execute("""
			select
				COALESCE(admin.semester, (SELECT c.semester FROM course c LIMIT 1)) AS semester
			from
				admin_settings admin
		""", None, True)
		# parse row
		default_semester = result[0]['semester'] ## Only one record in table for admin_settings
		if error:
			return (None, error)
		else:
			return (default_semester, error)

	def set_semester_default(self, semester):
		try:
			cmd = """
				UPDATE
					admin_settings
				SET
					semester = %s
			"""
			response, error = self.db_conn.execute(cmd, [semester], False)

		except Exception as e:
			# self.db_conn.rollback()
			return (False, e)

		if response != None:
			return(True, None)
		else:
			return (False, error)
