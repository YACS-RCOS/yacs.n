#!/usr/bin/env bash
psql -d yacs < schema/course.sql
psql -d yacs < schema/course_session.sql
