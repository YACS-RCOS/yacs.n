#!/usr/bin/python3
from flask import Flask
from flask import send_from_directory
from flask import jsonify
from flask import Response
from flask import request
from flask import redirect
from flask import url_for
import db.connection as connection
import db.classinfo as ClassInfo
import db.courses as Courses
import db.semester_date_mapping as DateMapping
import db.admin as AdminInfo
import db.student_course_selection as CourseSelect
import controller.user as user_controller
import controller.session as session_controller
import controller.userevent as event_controller
from io import StringIO
import json
import os


# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
courses = Courses.Courses(db_conn)
date_range_map = DateMapping.semester_date_mapping(db_conn)
admin_info = AdminInfo.Admin(db_conn)
course_select = CourseSelect.student_course_selection(db_conn)

app = Flask(__name__)

@app.route('/')
def root():
    return "YACS API is Up!"

@app.route('/api/')
def apiroot():
    return "wow"

# - data routes

@app.route('/api/class', methods=['GET'])
def get_classes():
    classes, error = class_info.get_classes_full()
    return jsonify(classes) if not error else Response(error, status=500)


@app.route('/api/department', methods=['GET'])
def get_departments():
    departments, error = class_info.get_departments()
    return jsonify(departments) if not error else Response(error, status=500)


@app.route('/api/subsemester', methods=['GET'])
def get_subsemesters():
    subsemesters, error = class_info.get_subsemesters()
    return jsonify(subsemesters) if not error else Response(error, status=500)

@app.route('/api/semester', methods=['GET'])
def get_semesters():
    semesters, error = class_info.get_semesters()
    return jsonify(semesters) if not error else Response(error, status=500)

@app.route('/api/defaultsemester', methods=['GET'])
def get_defaultSemester():
    semester, error = admin_info.get_semester_default()
    return jsonify(semester) if not error else Response(error, status=500)

@app.route('/api/defaultsemesterset', methods=['POST'])
def set_defaultSemester():
    info = request.get_json()
    success, error = admin_info.set_semester_default(info['default'])
    if success:
        return Response(status=200)
    else:
        print(error)
        return Response(error.__str__(), status=500)

@app.route('/api/bulkCourseUpload', methods=['POST'])
def uploadHandler():
    # check for user files
    if not request.files:
        return Response("No file received", 400)
    if request.files['file'].filename.rsplit('.', 1)[1].lower() != 'csv':
        return Response("File must have csv extension", 400)
    # get file
    csv_file = StringIO(request.files['file'].read().decode())
    isSuccess, error = courses.populate_from_csv(csv_file)
    if (isSuccess):
        return Response(status=200)
    else:
        print(error)
        return Response(error.__str__(), status=500)

@app.route('/api/mapDateRangeToSemesterPart', methods=['POST'])
def map_date_range_to_semester_part_handler():
    # This depends on date_start, date_end, and semester_part_name being
    # ordered since each field has multiple entries. They should be ordered
    # as each dict entry has the value of list. But if it doesn't work,
    # look into request.parameter_storage_class which will change the default
    # ImmutableMultiDict class that request.form uses. https://flask.palletsprojects.com/en/1.0.x/patterns/subclassing/
    if (request.form):
        semester_part_names = request.form.getlist('semester_part_name')
        start_dates = request.form.getlist('date_start')
        end_dates = request.form.getlist('date_end')
        if (start_dates and end_dates and semester_part_names):
            _, error = date_range_map.insert_all(start_dates, end_dates, semester_part_names)
            if (not error):
                return Response(status=200)
            else:
                return Response(error, status=500)
    return Response("Did not receive proper form data", status=500)


# - user system api
@app.route('/api/user', methods=['GET'])
def get_user_info():
    return user_controller.get_user_info(request.json)


@app.route('/api/user', methods=['POST'])
def add_user():
    return user_controller.add_user(request.json)


@app.route('/api/user', methods=['DELETE'])
def delete_user():
    return user_controller.delete_user(request.json)


@app.route('/api/user', methods=['PUT'])
def update_user_info():
    return user_controller.update_user(request.json)


@app.route('/api/session', methods=['POST'])
def log_in():
    return session_controller.add_session(request.json)


@app.route('/api/session', methods=['DELETE'])
def log_out():
    return session_controller.delete_session(request.json)


@app.route('/api/event', methods=['POST'])
def add_user_event():
    return event_controller.add_event(json.loads(request.data))

@app.route('/api/addcourse', methods=['POST'])
def add_student_course():
    info = request.json

@app.route('/api/removecourse', methods=['POST'])
def remove_student_course():
    info = request.json

@app.route('/api/getcourses', methods=['GET'])
def get_student_courses():
    info = request.json


if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', 'True'), host='0.0.0.0', port=5000)
