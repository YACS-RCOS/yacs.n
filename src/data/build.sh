#!/usr/bin/env bash
psql -d yacs < schema/course.sql
psql -d yacs < schema/course_session.sql
psql -d yacs < schema/semester_date_range.sql
psql -d yacs < schema/admin_setting.sql