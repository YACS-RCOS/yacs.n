DROP TABLE IF EXISTS student_course_selection;
CREATE TABLE student_course_selection
(
	user_id		int,
	semester	varchar(255),
	course_name	varchar(255),
	crn 		varchar(255),

	PRIMARY KEY (user_id, semester, course_name, crn),
	FOREIGN KEY (user_id) REFERENCES user_account(user_id)
);

