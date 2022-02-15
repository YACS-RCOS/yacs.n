#!/usr/bin/python3
from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, Form, File
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel

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
"""
NOTE: on caching
on add of semester of change of data from GET
do a cache.clear() to ensure data integrity
"""
# cache = Cache(config={'CACHE_TYPE': 'simple'})

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=os.environ.get("FLASK_SIGN_KEY", "localTestingKey"))
# app.secret_key = os.environ.get("FLASK_SIGN_KEY", "localTestingKey")
# cache.init_app(app)

class Cache:
    def clear(self):
        pass

# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
courses = Courses.Courses(db_conn, Cache()) #, cache)
date_range_map = DateMapping.semester_date_mapping(db_conn)
admin_info = AdminInfo.Admin(db_conn)
course_select = CourseSelect.student_course_selection(db_conn)
semester_info = SemesterInfo.semester_info(db_conn)
users = UserModel.User()

def is_admin_user():
    if 'user' in session and (session['user']['admin'] or session['user']['super_admin']):
        return True
    return False

@app.get('/')
# @cache.cached(timeout=Constants.HOUR_IN_SECONDS)
def root():
    return Response(content='YACS API is Up!',)

@app.get('/api')
def apiroot():
    return Response(content='wow')

# - data routes
#
# @app.route('/api/class', methods=['GET'])
# @cache.cached(timeout=Constants.HOUR_IN_SECONDS, query_string=True)
# def get_classes():
#     """
#     GET /api/class?semester={}&search={}
#     Cached: 1 Hour
#     """
#     semester = request.args.get("semester", default=None)
#     search  = request.args.get("search", default=None)
#     if semester:
#         if not semester_info.is_public(semester):
#             if is_admin_user():
#                 classes, error = class_info.get_classes_full(semester)
#                 return jsonify(classes) if not error else Response(error, status=500)
#             return Response("Semester isn't available", status=401)
#         if search is not None:
#             classes, error = class_info.get_classes_by_search(semester, search)
#         else:
#             classes, error = class_info.get_classes_full(semester)
#         return jsonify(classes) if not error else Response(error, status=500)
#     return Response("missing semester option", status=400)
# @app.route('/api/department', methods=['GET'])
# @cache.cached(timeout=Constants.HOUR_IN_SECONDS)
# def get_departments():
#     """
#     GET /api/department
#     Cached: 1 Hour
#
#     List of departments i.e. COGS, CIVL, CSCI, BIOL
#     """
#     departments, error = class_info.get_departments()
#     return jsonify(departments) if not error else Response(error, status=500)
#
# @app.route('/api/subsemester', methods=['GET'])
# @cache.cached(timeout=Constants.HOUR_IN_SECONDS, query_string=True)
# def get_subsemesters():
#     """
#     GET /api/subsemester?semester={}
#     Cached: 1 Hour
#
#     Get list of departments i.e. COGS, CIVL, CSCI, BIOL
#     (Used in dropdown in "Course Search"
#     """
#     semester = request.args.get("semester", default=None)
#     if semester:
#         subsemesters, error = class_info.get_subsemesters(semester)
#         return jsonify(subsemesters) if not error else Response(error, status=500)
#     # Some cases, we do want all subsemesters across all semesters like in Admin Panel
#     subsemesters, error = class_info.get_subsemesters()
#     return jsonify(subsemesters) if not error else Response(error, status=500)

@app.get('/api/semester')
# @cache.cached(timeout=Constants.DAY_IN_SECONDS)
def get_semesters():
    """
    GET /api/semester
    Cached: 24 Hours
    """
    semesters, error = class_info.get_semesters()
    return Response(content=json.dumps([dict(row) for row in semesters])) if not error else Response(error, status_code=500)

# @app.route('/api/semesterInfo', methods=['GET'])
# def get_all_semester_info():
#     all_semester_info, error = class_info.get_all_semester_info()
#     return jsonify(all_semester_info) if not error else Response(error, status=500)
#
# @app.route('/api/defaultsemester', methods=['GET'])
# def get_defaultSemester():
#     semester, error = admin_info.get_semester_default()
#     return jsonify(semester) if not error else Response(error, status=500)
#
# @app.route('/api/defaultsemesterset', methods=['POST'])
# def set_defaultSemester():
#     info = request.get_json()
#     success, error = admin_info.set_semester_default(info['default'])
#     if success:
#         return Response(status=200)
#     else:
#         print(error)
#         return Response(error.__str__(), status=500)

#Parses the data from the .csv data files
@app.post('/api/bulkCourseUpload')
async def uploadHandler(
        isPubliclyVisible: str = Form(...),
        file: UploadFile = File(...) ):
    # check for user files
    print("received file " + str(file.filename))
    if not file:
        return Response("No file received", 400)
    if file.filename.find('.') == -1 or file.filename.rsplit('.', 1)[1].lower() != 'csv':
        return Response("File must have csv extension", 400)
    # get file
    contents = await file.read()
    csv_file = StringIO(contents.decode())
    # update semester infos based on isPubliclyVisible, hiding semester if needed
    # is_publicly_visible = request.form.get("isPubliclyVisible", default=False)
    semesters = pd.read_csv(csv_file)['semester'].unique()
    for semester in semesters:
        semester_info.upsert(semester, isPubliclyVisible)
    # Like C, the cursor will be at EOF after full read, so reset to beginning
    csv_file.seek(0)
    # Clear out course data of the same semester before population due to
    # data source (E.g. SIS & Acalog Catalog) possibly updating/removing/adding
    # courses.
    courses.bulk_delete(semesters=semesters)
    # Populate DB from CSV
    isSuccess, error = courses.populate_from_csv(csv_file)
    if (isSuccess):
        return Response(status_code=200)
    else:
        print(error)
        return Response(error.__str__(), status_code=500)

# @app.route('/api/mapDateRangeToSemesterPart', methods=['POST'])
# def map_date_range_to_semester_part_handler():
#     # This depends on date_start, date_end, and semester_part_name being
#     # ordered since each field has multiple entries. They should be ordered
#     # as each dict entry has the value of list. But if it doesn't work,
#     # look into request.parameter_storage_class which will change the default
#     # ImmutableMultiDict class that request.form uses. https://flask.palletsprojects.com/en/1.0.x/patterns/subclassing/
#     if (request.form):
#         # If checkbox is false, then, by design, it is not included in the form data.
#         is_publicly_visible = request.form.get('isPubliclyVisible', default=False)
#         semester_title = request.form.get('semesterTitle')
#         semester_part_names = request.form.getlist('semester_part_name')
#         start_dates = request.form.getlist('date_start')
#         end_dates = request.form.getlist('date_end')
#         if (start_dates and end_dates and semester_part_names and is_publicly_visible is not None and semester_title):
#             _, error = date_range_map.insert_all(start_dates, end_dates, semester_part_names)
#             semester_info.upsert(semester_title, is_publicly_visible)
#             if (not error):
#                 return Response(status=200)
#             else:
#                 return Response(error, status=500)
#     return Response("Did not receive proper form data", status=500)
#
#
# # - user system api
# @app.route('/api/user/<session_id>', methods=['GET'])
# def get_user_info(session_id):
#     if 'user' not in session:
#         return Response("Not authorized", status=403)
#
#     return user_controller.get_user_info(session_id)
#

class UserPydantic(BaseModel):
    email: str
    name: str
    phone: str
    password: str
    degree: str
    major: str

@app.post('/api/user')
def add_user(user: UserPydantic):
    return user_controller.add_user(user.dict())

#
# @app.route('/api/user', methods=['DELETE'])
# def delete_user():
#     if 'user' not in session:
#         return Response("Not authorized", status=403)
#
#     return user_controller.delete_user(request.json)
#
#
# @app.route('/api/user', methods=['PUT'])
# def update_user_info():
#     if 'user' not in session:
#         return Response("Not authorized", status=403)
#
#     return user_controller.update_user(request.json)
#

class SessionPydantic(BaseModel):
    email: str
    password: str

@app.post('/api/session')
def log_in(request: Request, credentials: SessionPydantic):
    session_res = session_controller.add_session(credentials.dict())
    if (session_res['success']):
        session_data = session_res['content']
        # [0] b/c conn.exec uses fetchall() which wraps result in list
        user = users.get_user(uid=session_data['uid'])[0]
        request.session['user'] = user
        # Session will last as long as the browser session.
        # request.session.max_age = None
    return session_res

class SessionDeletePydantic(BaseModel):
    sessionID: str

@app.delete('/api/session')
def log_out(request: Request, session: SessionDeletePydantic):
    response = session_controller.delete_session(session.dict())

    if response['success']:
        request.session.pop('user', None)

    return response


# @app.route('/api/event', methods=['POST'])
# def add_user_event():
#     return event_controller.add_event(json.loads(request.data))
#
# @app.route('/api/user/course', methods=['POST'])
# def add_student_course():
#     info = request.get_json()
#
#     if 'user' not in session:
#         return Response("Not authorized", status=403)
#
#     resp, error = course_select.add_selection(info['name'], info['semester'], session['user']['user_id'], info['cid'])
#     return Response(status=200) if not error else Response(error, status=500)
#
#
# @app.route('/api/user/course', methods=['DELETE'])
# def remove_student_course():
#     info = request.json
#
#     if 'user' not in session:
#         return Response("Not authorized", status=403)
#
#     resp, error = course_select.remove_selection(info['name'], info['semester'], session['user']['user_id'], info['cid'])
#     return Response(status=200) if not error else Response(error, status=500)
#
# @app.route('/api/user/course', methods=['GET'])
# def get_student_courses():
#     if 'user' not in session:
#         return Response("Not authorized", status=403)
#
#     courses, error = course_select.get_selection(session['user']['user_id'])
#     return jsonify(courses) if not error else Response(error, status=500)
#
# if __name__ == '__main__':
#     app.run(debug=os.environ.get('DEBUG', 'True'), host='0.0.0.0', port=5000)
