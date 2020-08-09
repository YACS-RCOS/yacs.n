#!/usr/bin/env bash
SCRIPTDIR=$(dirname "$BASH_SOURCE")
psql -d yacs < $SCRIPTDIR/schema/01_course.sql
psql -d yacs < $SCRIPTDIR/schema/02_course_session.sql
psql -d yacs < $SCRIPTDIR/schema/03_admin_setting.sql
psql -d yacs < $SCRIPTDIR/schema/04_semester_date_range.sql
psql -d yacs < $SCRIPTDIR/schema/05_course_corequisite.sql
psql -d yacs < $SCRIPTDIR/schema/06_course_prerequisite.sql
psql -d yacs < $SCRIPTDIR/schema/07_user_account.sql
psql -d yacs < $SCRIPTDIR/schema/08_user_session.sql
psql -d yacs < $SCRIPTDIR/schema/09_user_event.sql
psql -d yacs < $SCRIPTDIR/schema/10_student_course_selection.sql
psql -d yacs < $SCRIPTDIR/schema/11_semester_info.sql
psql -d yacs < $SCRIPTDIR/schema/12_degree_templates.sql
