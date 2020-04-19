class student_course_selection:
	def __init__(self, db_conn):
		self.db_conn = db_conn

	def add_selection(self, cid, sem, uid):
		try:
			sql = 	"""
					INSERT INTO
						student_course_selection (user_id, semester, course_id)
					VALUES
						(%s, %s, %s)
					"""
			resp, error = self.db_conn.execute(sql, [uid, sem, cid], False)
		
		except Exception as e:
			return (False, e)

		if error is not None:
			return (False, error)
		else:
			return (True, None)

	def remove_selection(self, cid, sem, uid):
		try:
			sql = 	"""
					DELETE FROM
						student_course_selection
					WHERE
						user_id = %s AND
						semester = %s AND
						course_id = %s
					"""
			resp, error = self.db_conn.execute(sql, [uid, sem, cid], False)

		except Exception as e:
			return (False, e)

		if error is not None:
			return (False, error)
		else:
			return (True, None)

	def get_selection(self, uid):
		# sqle = "SELECT EXISTS(SELECT * FROM student_course_selection WHERE user_id=%s)"
		# exists, e = self.db_conn.execute(sqle, [uid], True)
		# if exists:
		try:
			sql = """
					select
						course_id,
						semester
					from
						student_course_selection
					where
						user_id = %s
					order by
						course_id asc
					"""
			courses, error = self.db_conn.execute(sql, [uid], True)

		except Exception as e:
			return (False, e)

		if error is not None:
			return (False, error)
		else:
			return (courses, None)
	# else:
	# 	if e is not None:
	# 		return (False, e)
	# 	else:
	# 		return ([], None)