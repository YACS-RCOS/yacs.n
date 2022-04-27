from db.model import *


class Admin(Model):
	def __init__(self):
		super().__init__()

	async def get_semester_default(self):
		# NOTE: COALESCE takes first non-null vaue from the list
		sql = """
			SELECT admin.semester FROM admin_settings admin
			UNION ALL
			SELECT si.semester FROM semester_info si WHERE si.public=true::boolean
			LIMIT 1
		"""
		result, error = await self.db.execute(sql, [], True)

		default_semester = None
		if (len(result) == 1):
			default_semester = result[0]['semester']

		if error:
			return (None, error)
		else:
			return (default_semester, error)

	async def set_semester_default(self, semester):
		try:
			cmd = """
				WITH _ AS (DELETE FROM admin_settings)
				INSERT INTO admin_settings(semester)
				VALUES('%s')
				ON CONFLICT (semester) DO UPDATE SET semester = '%s'
			"""
			# response, error = await self.db.execute(cmd, (semester, semester), False)
			response, error = await self.db.execute(cmd, (semester,semester), False)

		except Exception as e:
			return (False, e)

		if response != None:
			return(True, None)
		else:
			return (False, error)
