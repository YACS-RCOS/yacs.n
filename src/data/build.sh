#!/usr/bin/env bash
psql -d yacs < schema/01_course.sql
psql -d yacs < schema/02_course_session.sql
psql -d yacs < schema/03_admin_setting.sql
psql -d yacs < schema/04_semester_date_range.sql
psql -d yacs < schema/05_course_corequisite.sql
psql -d yacs < schema/06_course_prerequisite.sql
psql -d yacs < schema/07_user.sql
psql -d yacs < schema/08_user_session.sql
psql -d yacs < schema/09_user_event.sql
psql -d yacs < schema/10_student_course_selection.sql