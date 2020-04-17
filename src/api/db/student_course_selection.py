class student_course_selection:
	def __init__(self, db_conn):
		self.db_conn = db_conn

	def add_selection(self, cid, sem, uid):
		sql = 	"""
				INSERT INTO
					student_course_selection (user_id, semester, course_id)
				VALUES
					(%d, %s, %s)
				"""
		self.db_conn.execute(sql, [uid, sem, cid], False)

	def remove_selection(self, cid, sem, uid):
		sql = 	"""
				DELETE FROM
					student_course_selection
				WHERE
					user_id = %d AND
					semester = %s AND
					course_id = %d
				"""
		self.db_conn.execute(sql, [uid, sem, cid], False)

	def get_selection(self, uid):
		sql = """
				select
					course_id
					semester
				from
					student_course_selection
				where
					user_id = %d
				group by
					semester
				"""
		return self.db_conn.execute(sql, [uid], True)
