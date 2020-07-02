#!/usr/bin/python3
from flask import Flask
from flask import send_from_directory
from flask import jsonify
from flask import Response
from flask import request
from flask import redirect
from flask import url_for
from flask import session
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


# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
courses = Courses.Courses(db_conn)
date_range_map = DateMapping.semester_date_mapping(db_conn)
admin_info = AdminInfo.Admin(db_conn)
course_select = CourseSelect.student_course_selection(db_conn)
semester_info = SemesterInfo.semester_info(db_conn)
users = UserModel.User()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SIGN_KEY", "localTestingKey")

def is_admin_user():
    if 'user' in session and (session['user']['admin'] or session['user']['super_admin']):
        return True
    return False

@app.route('/')
def root():
    return "YACS API is Up!"

@app.route('/api/')
def apiroot():
    return "wow"

# - data routes

@app.route('/api/class', methods=['GET'])
def get_classes():
    semester = request.args.get("semester", default=None)
    if semester:
        if not semester_info.is_public(semester):
            if is_admin_user():
                classes, error = class_info.get_classes_full(semester)
                return jsonify(classes) if not error else Response(error, status=500)
            return Response("Semester isn't available", status=401)
        classes, error = class_info.get_classes_full(semester)
        return jsonify(classes) if not error else Response(error, status=500)
    return Response("missing semester option", status=400)


@app.route('/api/department', methods=['GET'])
def get_departments():
    departments, error = class_info.get_departments()
    return jsonify(departments) if not error else Response(error, status=500)


@app.route('/api/subsemester', methods=['GET'])
def get_subsemesters():
    semester = request.args.get("semester", default=None)
    if semester:
        subsemesters, error = class_info.get_subsemesters(semester)
        return jsonify(subsemesters) if not error else Response(error, status=500)
    # Some cases, we do want all subsemesters across all semesters like in Admin Panel
    subsemesters, error = class_info.get_subsemesters()
    return jsonify(subsemesters) if not error else Response(error, status=500)

@app.route('/api/semester', methods=['GET'])
def get_semesters():
    if is_admin_user():
        semesters, error = class_info.get_semesters(includeHidden=True)
        return jsonify(semesters) if not error else Response(error, status=500)
    semesters, error = class_info.get_semesters()
    return jsonify(semesters) if not error else Response(error, status=500)


@app.route('/api/semesterInfo', methods=['GET'])
def get_all_semester_info():
    all_semester_info, error = class_info.get_all_semester_info()
    return jsonify(all_semester_info) if not error else Response(error, status=500)

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
    # update semester infos based on isPubliclyVisible, hiding semester if needed
    is_publicly_visible = request.form.get("isPubliclyVisible", default=False)
    semesters = pd.read_csv(csv_file)['semester'].unique()
    for semester in semesters:
        semester_info.upsert(semester, is_publicly_visible)
    # Like C, the cursor will be at EOF after full read, so reset to beginning
    csv_file.seek(0)
    # Clear out course data of the same semester before population due to
    # data source (E.g. SIS & Acalog Catalog) possibly updating/removing/adding
    # courses.
    courses.bulk_delete(semesters=semesters)
    # Populate DB from CSV
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
        # If checkbox is false, then, by design, it is not included in the form data.
        is_publicly_visible = request.form.get('isPubliclyVisible', default=False)
        semester_title = request.form.get('semesterTitle')
        semester_part_names = request.form.getlist('semester_part_name')
        start_dates = request.form.getlist('date_start')
        end_dates = request.form.getlist('date_end')
        if (start_dates and end_dates and semester_part_names and is_publicly_visible is not None and semester_title):
            _, error = date_range_map.insert_all(start_dates, end_dates, semester_part_names)
            semester_info.upsert(semester_title, is_publicly_visible)
            if (not error):
                return Response(status=200)
            else:
                return Response(error, status=500)
    return Response("Did not receive proper form data", status=500)

@app.route('/api/search', methods=['GET'])
def get_courses_by_search():
    semester = request.args.get("semester", default=None)
    search = request.args.get("search", default=None)
    if semester:
        courses, error = class_info.get_courses_by_search(semester, search)
        return jsonify(courses) if not error else Response(error, status=500)
    return Response("missing semester option", status=500)


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
    session_res = session_controller.add_session(request.json).json
    if (session_res['success']):
        session_data = session_res['content']
        # [0] b/c conn.exec uses fetchall() which wraps result in list
        user = users.get_user(uid=session_data['uid'])[0]
        session['user'] = user
        # https://flask.palletsprojects.com/en/1.1.x/api/?highlight=session#flask.session.permanent
        session.permanent = False
    return session_res


@app.route('/api/session', methods=['DELETE'])
def log_out():
    session.pop('user', None)
    return session_controller.delete_session(request.json)


@app.route('/api/event', methods=['POST'])
def add_user_event():
    return event_controller.add_event(json.loads(request.data))

@app.route('/api/course', methods=['POST'])
def add_student_course():
    info = request.get_json()
    resp, error = course_select.add_selection(info['name'], info['semester'], info['uid'], info['cid'])
    return Response(status=200) if not error else Response(error, status=500)


@app.route('/api/course', methods=['DELETE'])
def remove_student_course():
    info = request.json
    resp, error = course_select.remove_selection(info['name'], info['semester'], info['uid'], info['cid'])
    return Response(status=200) if not error else Response(error, status=500)

@app.route('/api/course', methods=['GET'])
def get_student_courses():
    info = request.args
    courses, error = course_select.get_selection(info['uid'])
    return jsonify(courses) if not error else Response(error, status=500)

if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', 'True'), host='0.0.0.0', port=5000)