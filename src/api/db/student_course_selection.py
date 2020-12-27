class student_course_selection:
	def __init__(self, db_conn):
		self.db_conn = db_conn

	def add_selection(self, name, sem, uid, cid):
		sql = 	"""
				INSERT INTO
					student_course_selection (user_id, semester, course_id, crn)
				VALUES
					(%s, %s, %s, %s)
				ON CONFLICT DO NOTHING;
				"""
		resp, error = self.db_conn.execute(sql, [uid, sem, name, cid], False)
		return (True, None) if not error else (False, error)

	def remove_selection(self, name, sem, uid, cid):
		if cid is None:
			sql = 	"""
					DELETE FROM
						student_course_selection
					WHERE
						user_id = %s AND
						semester = %s AND
						course_id = %s
					"""
			resp, error = self.db_conn.execute(sql, [uid, sem, name], False)
		else:
			sql = 	"""
					DELETE FROM
						student_course_selection
					WHERE
						user_id = %s AND
						semester = %s AND
						course_id = %s AND
						crn = %s

					"""
			resp, error = self.db_conn.execute(sql, [uid, sem, name, cid], False)

		return (True, None) if not error else (False, error)

	def get_selection(self, uid):
		sql = """
				select
					course_id,
					semester,
					crn
				from
					student_course_selection
				where
					user_id = %s
				order by
					course_id asc,
					crn
				"""
		courses, error = self.db_conn.execute(sql, [uid], True)
		return (courses, None) if not error else (False, error)
