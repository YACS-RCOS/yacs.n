#!/usr/bin/env bash
SCRIPTDIR=$(dirname "$BASH_SOURCE")
psql -d yacs < $SCRIPTDIR/schema/course.sql
psql -d yacs < $SCRIPTDIR/schema/course_session.sql
psql -d yacs < $SCRIPTDIR/schema/admin_setting.sql
psql -d yacs < $SCRIPTDIR/schema/semester_date_range.sql
psql -d yacs < $SCRIPTDIR/schema/semester_info.sql
psql -d yacs < $SCRIPTDIR/schema/course_corequisite.sql
psql -d yacs < $SCRIPTDIR/schema/course_prerequisite.sql
psql -d yacs < $SCRIPTDIR/schema/user.sql
psql -d yacs < $SCRIPTDIR/schema/user_session.sql
psql -d yacs < $SCRIPTDIR/schema/user_event.sql