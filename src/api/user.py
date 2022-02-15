from flask import Flask                 #https://flask.palletsprojects.com/
from flask import send_from_directory       #Documentation for the flask library
from flask import jsonify
from flask import Response
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_caching import Cache
import db.connection as connection
import db.classinfo as ClassInfo
import db.courses as Courses
import db.semester_info as SemesterInfo
import db.semester_date_mapping as DateMapping
import db.admin as AdminInfo
import db.student_course_selection as CourseSelect
import db.user as UserModel
import controller.user as user_controller
import controller.session as session_controller
import controller.userevent as event_controller
from io import StringIO
import json
import os
import pandas as pd
from constants import Constants
@app.route('/api/user', methods=['POST'])
def add_user():
    return user_controller.add_user(request.json)


@app.route('/api/user', methods=['DELETE'])
def delete_user():
    if 'user' not in session:
        return Response("Not authorized", status=403)
    return user_controller.delete_user(request.json)
