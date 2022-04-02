#!/usr/bin/python3
from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, Form, File, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from fastapi import Depends

from api_models import *
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

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=os.environ.get("FLASK_SIGN_KEY", "localTestingKey"))

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
courses = Courses.Courses(db_conn, FastAPICache)
date_range_map = DateMapping.semester_date_mapping(db_conn)
admin_info = AdminInfo.Admin(db_conn)
course_select = CourseSelect.student_course_selection(db_conn)
semester_info = SemesterInfo.semester_info(db_conn)
users = UserModel.User()

def is_admin_user(session):
    if 'user' in session and (session['user']['admin'] or session['user']['super_admin']):
        return True
    return False

@app.get('/')
@cache(expire=Constants.HOUR_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def root(request: Request):
    return Response(content='YACS API is Up!',)

@app.get('/api')
def apiroot():
    return Response(content='wow')

@app.get('/api/class')
@cache(expire=Constants.HOUR_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def get_classes(request: Request, semester: str or None = None, search: str or None = None):
    """
    GET /api/class?semester={}&search={}
    Cached: 1 Hour
    """
    if semester:
        if not semester_info.is_public(semester):
            if is_admin_user(request.session):
                classes, error = class_info.get_classes_full(semester)
                return classes if not error else Response(error, status_code=500)
            return Response(content="Semester isn't available", status_code=401)
        if search is not None:
            classes, error = class_info.get_classes_by_search(semester, search)
        else:
            classes, error = class_info.get_classes_full(semester)
        return classes if not error else Response(error, status_code=500)
    return Response(content="missing semester option", status_code=400)
    
@app.get('/api/department')
@cache(expire=Constants.HOUR_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def get_departments():
    """
    GET /api/department
    Cached: 1 Hour
 
    List of departments i.e. COGS, CIVL, CSCI, BIOL
    """
    departments, error = class_info.get_departments()
    return departments if not error else Response(content=error, status_code=500)

@app.get('/api/subsemester')
@cache(expire=Constants.HOUR_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def get_subsemesters(subsemester: SubsemesterPydantic = Depends(SubsemesterPydantic)):
    """
    GET /api/subsemester?semester={}
    Cached: 1 Hour

    Get list of departments i.e. COGS, CIVL, CSCI, BIOL
    (Used in dropdown in "Course Search"
    """
    if subsemester.semester:
        subsemesters, error = class_info.get_subsemesters(subsemester.semester)
        # for i in subsemesters:
        #     print(i)
        db_list = [dict(r) for r in subsemesters]
        return db_list if not error else Response(error, status_code=500)
    # Some cases, we do want all subsemesters across all semesters like in Admin Panel
    subsemesters, error = class_info.get_subsemesters()
    db_list = [dict(r) for r in subsemesters]
    return db_list if not error else Response(error, status_code=500)

@app.get('/api/semester')
@cache(expire=Constants.DAY_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def get_semesters():
    """
    GET /api/semester
    Cached: 24 Hours
    """
    semesters, error = class_info.get_semesters()
    db_list = [dict(r) for r in semesters]
    return db_list if not error else Response(error, status_code=500)

@app.get('/api/semesterInfo')
def get_all_semester_info():
    all_semester_info, error = class_info.get_all_semester_info()
    return all_semester_info if not error else Response(error, status=500)

@app.get('/api/defaultsemester')
def get_defaultSemester():
    semester, error = admin_info.get_semester_default()
    return semester if not error else Response(error, status=500)


@app.post('/api/defaultsemesterset')
def set_defaultSemester(semester_set: DefaultSemesterSetPydantic):
    success, error = admin_info.set_semester_default(semester_set.default)
    if success:
        return Response(status_code=200)
    else:
        print(error)
        return Response(error.__str__(), status_code=500)

#Parses the data from the .csv data files
@app.post('/api/bulkCourseUpload')
async def uploadHandler(
        isPubliclyVisible: str = Form(...),
        file: UploadFile = File(...)):
    # check for user files
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

@app.post('/api/mapDateRangeToSemesterPart')
async def map_date_range_to_semester_part_handler(request: Request):
     # This depends on date_start, date_end, and semester_part_name being
     # ordered since each field has multiple entries. They should be ordered
     # as each dict entry has the value of list. But if it doesn't work,
     # look into parameter_storage_class which will change the default
     # ImmutableMultiDict class that form uses. https://flask.palletsprojects.com/en/1.0.x/patterns/subclassing/
     form = await request.form()
     if (form):
         # If checkbox is false, then, by design, it is not included in the form data.
         is_publicly_visible = form.get('isPubliclyVisible', default=False)
         semester_title = form.get('semesterTitle')
         semester_part_names = form.getlist('semester_part_name')
         start_dates = form.getlist('date_start')
         end_dates = form.getlist('date_end')
         if (start_dates and end_dates and semester_part_names and is_publicly_visible is not None and semester_title):
             _, error = date_range_map.insert_all(start_dates, end_dates, semester_part_names)
             semester_info.upsert(semester_title, is_publicly_visible)
             if (not error):
                 return Response(status_code=200)
             else:
                 return Response(error, status_code=500)
     return Response("Did not receive proper form data", status_code=500)

#@app.route('/api/user/course', methods=['GET'])
@app.get('/api/user/course')
async def get_student_courses(request: Request):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    courses, error = course_select.get_selection(request.session['user']['user_id'])
    return courses if not error else Response(error, status_code=500)


# # - user system api
# @app.route('/api/user/<session_id>', methods=['GET'])
# def get_user_info(session_id):
#     if 'user' not in session:
#         return Response("Not authorized", status=403)

#     return user_controller.get_user_info(session_id)

@app.get('/api/user/{session_id}')
async def get_user_info(request: Request, session_id):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.get_user_info(session_id)


#
@app.post('/api/user')
async def add_user(user: UserPydantic):
    return user_controller.add_user(user.dict())

@app.delete('/api/user')
async def delete_user(request: Request, session: UserDeletePydantic):

    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.delete_user(session.dict())

# @app.route('/api/user', methods=['PUT'])
# def update_user_info():
#     if 'user' not in session:
#         return Response("Not authorized", status=403)
#
#     return user_controller.update_user(request.json)


@app.put('/api/user')
async def update_user_info(request:Request, user:updateUser):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.update_user(user)


@app.post('/api/session')
async def log_in(request: Request, credentials: SessionPydantic):
    session_res = session_controller.add_session(credentials.dict())
    if (session_res['success']):
        session_data = session_res['content']
        # [0] b/c conn.exec uses fetchall() which wraps result in list
        user = users.get_user(uid=session_data['uid'])[0]
        request.session['user'] = user
    return session_res

@app.delete('/api/session')
def log_out(request: Request, session: SessionDeletePydantic):
    response = session_controller.delete_session(session.dict())

    if response['success']:
        request.session.pop('user', None)

    return response

@app.post('/api/event')
def add_user_event(request: Request, credentials: SessionPydantic):
    return Response(status_code=501)
    #return event_controller.add_event(json.loads(request.data))

@app.post('/api/user/course')
async def add_student_course(request: Request, credentials: UserCoursePydantic):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)
    resp, error = course_select.add_selection(credentials.name, credentials.semester, request.session['user']['user_id'], credentials.cid)
    return Response(status_code=200) if not error else Response(error, status_code=500)


@app.delete('/api/user/course')
async def remove_student_course(request: Request, courseDelete:CourseDeletePydantic):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)
    resp,error = course_select.remove_selection(courseDelete.name, courseDelete.semester, request.session['user']['user_id'], courseDelete.cid)
    # resp, error = course_select.remove_selection(info['name'], info['semester'], session['user']['user_id'], info['cid'])
    return Response(status_code=200) if not error else Response(error, status_code=500)


