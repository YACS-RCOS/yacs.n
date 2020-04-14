DROP TABLE IF EXISTS student_course_selection;
CREATE TABLE student_course_selection
(
	user_id		int,
	semester	varchar(255),
	crn			varchar(255),

	PRIMARY KEY (user_id, semester),
	FOREIGN KEY (user_id) REFERENCES user_account(user_id)
);

INSERT INTO student_course_selection (user_id) (
    SELECT DISTINCT
        user_id
    FROM
        user_account
);

