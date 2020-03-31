#!/usr/bin/env bash
psql -d yacs << EOF
drop table course;
drop table course_session;
drop table admin_settings;
drop table semester_date_range;
EOF
