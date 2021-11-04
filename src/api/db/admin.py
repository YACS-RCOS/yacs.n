class Admin:

	def __init__(self, db_conn):
		self.db_conn = db_conn
		self.interface_name = 'admin_info'

	def get_semester_default(self):
		# NOTE: COALESCE takes first non-null vaue from the list
		result, error = self.db_conn.execute("""
			SELECT admin.semester FROM admin_settings admin
			UNION ALL
			SELECT si.semester FROM semester_info si WHERE si.public=true::boolean
			LIMIT 1
		""", None, True)

		default_semester = None

		if len(result) == 1:
			# parse row
			default_semester = result[0]['semester'] ## Only one record in table for admin_settings

		if error:
			return (None, error)
		else:
			return (default_semester, error)

	def set_semester_default(self, semester):
		try:
			cmd = """
				WITH _ AS (DELETE FROM admin_settings)
				INSERT INTO admin_settings(semester)
				VALUES(%s)
				ON CONFLICT (semester) DO UPDATE SET semester = %s
			"""
			response, error = self.db_conn.execute(cmd, [semester, semester], False)

		except Exception as e:
			# self.db_conn.rollback()
			return (False, e)

		if response != None:
			return(True, None)
		else:
			return (False, error)
