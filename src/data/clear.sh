#!/usr/bin/env bash
psql -d yacs << EOF
drop table course;
drop table course_session;
EOF
