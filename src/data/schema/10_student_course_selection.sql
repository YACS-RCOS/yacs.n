DROP TABLE IF EXISTS student_course_selection;
CREATE TABLE student_course_selection
(
	user_id		int,
	semester	varchar(255),
	course_id	varchar(255),

	PRIMARY KEY (user_id, semester, course_id),
	FOREIGN KEY (user_id) REFERENCES user_account(user_id)
);

-- INSERT INTO student_course_selection (user_id, semester, course_id) 
-- VALUES (
--     (SELECT DISTINCT
--         user_id
--     FROM
--         user_account), 
--     (SELECT DISTINCT
--     	semester
--     FROM
--     	admin_settings),
--     LIFE-101
-- );

