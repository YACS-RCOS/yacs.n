from curses import A_ALTCHARSET
from db.model import *


# class User(Model):
#     def __init__(self):
#         super().__init__()

class AdminSetting(Model):
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
		args = None
		result = await self.db.execute(sql, [], True)
		if (result == None):
			return None
		else:
			result = result[0]['semester']
			return result


		# default_semester = None

		# if len(result) == 1:
		# 	# parse row
		# 	default_semester = result[0]['semester'] ## Only one record in table for admin_settings

		# # if error:
		# # 	return (None, error)
		# # else:
		# # 	return (default_semester, error)
		# return result

	async def set_semester_default(self, semester):
		try:
			cmd = """
				WITH _ AS (DELETE FROM admin_settings)
				INSERT INTO admin_settings(semester)
				VALUES('%s')
				ON CONFLICT (semester) DO UPDATE SET semester = '%s'
			"""
			# response, error = await self.db.execute(cmd, (semester, semester), False)
			result = await self.db.execute(cmd, (semester,semester), False)
			return result[0]

		except Exception as e:
			# self.db_conn.rollback()
			return (False, e)

		if response != None:
			return(True, None)
		else:
			return (False, error)
