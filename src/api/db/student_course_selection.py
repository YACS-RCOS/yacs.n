from db.model import *

class student_course_selection(Model):
	def __init__(self):
		super().__init__()

	async def add_selection(self, name, sem, uid, cid):
		print("DEBUG - add_selection", name, sem, uid, cid)
		sql = 	"""
				INSERT INTO
					student_course_selection (user_id, semester, course_name, crn)
				VALUES
					('%s', '%s', NULLIF($course$%(course_name)s$course$, ''), '%s'
					
					)
				ON CONFLICT DO NOTHING;
				"""
		resp, error = await self.db.execute(sql, [uid, sem, name, cid], False)
		return (True, None) if not error else (False, error)

	async def remove_selection(self, name, sem, uid, cid):
		if cid is None:
			sql = 	"""
					DELETE FROM
						student_course_selection
					WHERE
						user_id = '%s' AND
						semester = '%s' AND
						course_name = $course$%s$course$
					"""
			resp, error = await self.db.execute(sql, [uid, sem, name], False)
		else:
			sql = 	"""
					DELETE FROM
						student_course_selection
					WHERE
						user_id = '%s' AND
						semester = '%s' AND
						course_name = $course$%s$course$ AND
						crn = '%s'

					"""
			resp, error = await self.db.execute(sql, [uid, sem, name, cid], False)

		return (True, None) if not error else (False, error)

	async def get_selection(self, uid):
		sql = """
				select
					course_name,
					semester,
					crn
				from
					student_course_selection
				where
					user_id = '%s'
				order by
					course_name asc,
					crn
				"""
		courses, error = await self.db.execute(sql, [uid], True)
		return (courses, None) if not error else (False, error)
