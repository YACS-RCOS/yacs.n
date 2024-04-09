#!/usr/bin/python3
import json
import os
from io import StringIO
from fastapi import FastAPI, Request, Response, UploadFile, Form, File, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder

from api_models import *
from db import connection
import db.classinfo as ClassInfo
import db.courses as Courses
import db.professor as All_professors
import db.semester_info as SemesterInfo
import db.semester_date_mapping as DateMapping
import db.admin as AdminInfo
import db.student_course_selection as CourseSelect
import db.user as UserModel
import db.finals as Finals
import controller.user as user_controller
import controller.session as session_controller
import pandas as pd
from constants import Constants

#NOTE: on caching
#on add of semester of change of data from GET
#do a cache.clear() to ensure data integrity

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=os.environ.get("API_SIGN_KEY", "localTestingKey"))

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
courses = Courses.Courses(db_conn, FastAPICache)
date_range_map = DateMapping.SemesterDateMapping(db_conn)
admin_info = AdminInfo.Admin(db_conn)
course_select = CourseSelect.StudentCourseSelection(db_conn)
semester_info = SemesterInfo.SemesterInfo(db_conn)
professor_info = All_professors.Professor(db_conn, FastAPICache)
finals_info = Finals.Finals(db_conn)
users = UserModel.User()

def is_admin_user(session):
    if 'user' in session and (session['user']['admin'] or session['user']['super_admin']):
        return True
    return False

@app.get('/')
@cache(expire=Constants.HOUR_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def root(_request: Request):
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
    return all_semester_info if not error else Response(error, status_code=500)

@app.get('/api/defaultsemester')
def get_default_semester():
    semester, error = admin_info.get_semester_default()
    print(semester)
    return semester if not error else Response(error, status_code=500)


@app.post('/api/defaultsemesterset')
def set_default_semester(semester_set: DefaultSemesterSetPydantic):
    success, error = admin_info.set_semester_default(semester_set.default)
    if success:
        return Response(status_code=200)
    print(error)
    return Response(str(error), status_code=500)

#Parses the data from the .csv data files
@app.post('/api/bulkCourseUpload')
async def upload_handler(
        is_publicly_visible: str = Form(...),
        file: UploadFile = File(...)):
    # check for user files
    print("in process")
    if not file:
        return Response("No file received", 400)
    if file.filename.find('.') == -1 or file.filename.rsplit('.', 1)[1].lower() != 'csv':
        return Response("File must have csv extension", 400)
    # get file
    contents = await file.read()
    csv_file = StringIO(contents.decode())
    # update semester infos based on is_ublicly_visible, hiding semester if needed
    # is_publicly_visible = request.form.get("is_publicly_visible", default=False)
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
    is_success, error = courses.populate_from_csv(csv_file)
    if is_success:
        return Response(status_code=200)
    print(error)
    return Response(str(error), status_code=500)

@app.post('/api/bulkProfessorUpload')
async def upload_json(
        #_is_publicly_visible: str = Form(...),
        file: UploadFile = File(...)):
    # Check to make sure the user has sent a file
    if not file:
        return Response("No file received", 400)

    # Check that we receive a JSON file
    if file.filename.find('.') == -1 or file.filename.rsplit('.', 1)[1].lower() != 'json':
        return Response("File must have JSON extension", 400)

    # Get file contents
    contents = await file.read()

    # Load JSON data
    try:
        #convert string to python dict
        json_data = json.loads(contents.decode('utf-8'))
        # print(json_data)
    except json.JSONDecodeError as e:
        return Response(f"Invalid JSON data: {str(e)}", 400)

    # Call populate_from_json method
    is_success, error = professor_info.populate_from_json(json_data)
    if is_success:
        print("SUCCESS")
        return Response(status_code=200)
    print("NOT WORKING")
    print(error)
    return Response(str(error), status_code=500)

@app.post('/api/bulkFinalJsonUpload')
async def upload_finals_json(file: UploadFile = File(...), semester: str = Form(...)):
    # Check to make sure the user has sent a file
    if not file:
        return Response("No file received", 400)

    # Check that we receive a JSON file
    if file.filename.find('.') == -1 or file.filename.rsplit('.', 1)[1].lower() != 'json':
        return Response("File must have JSON extension", 400)

    # Get file contents
    contents = await file.read()

    # Load JSON data
    try:
        #convert string to python dict
        json_data = json.loads(contents.decode('utf-8'))
        # print(json_data)
    except json.JSONDecodeError as e:
        return Response(f"Invalid JSON data: {str(e)}", 400)

    # Delete old data
    finals_info.remove_semester_finals(semester)

    # Call populate_from_json method
    (is_success, error) = finals_info.populate_from_json(json_data, semester)
    if is_success:
        print("SUCCESS")
        return Response(status_code=200)
    print("NOT WORKING")
    print(error)
    return Response(str(error), status_code=500)


@app.post('/api/mapDateRangeToSemesterPart')
async def map_date_range_to_semester_part_handler(request: Request):
    # This depends on date_start, date_end, and semester_part_name being
    # ordered since each field has multiple entries. They should be ordered
    # as each dict entry has the value of list. But if it doesn't work,
    # look into parameter_storage_class which will change the default
    # ImmutableMultiDict class that form uses.
    # https://flask.palletsprojects.com/en/1.0.x/patterns/subclassing/
    form = await request.form()
    if form:
        # If checkbox is false, then, by design, it is not included in the form data.
        is_publicly_visible = form.get('is_publicly_visible', default=False)
        semester_title = form.get('semesterTitle')
        semester_part_names = form.getlist('semester_part_name')
        start_dates = form.getlist('date_start')
        end_dates = form.getlist('date_end')
        if start_dates and end_dates and semester_part_names \
        and is_publicly_visible is not None and semester_title:
            _, error = date_range_map.insert_all(start_dates, end_dates, semester_part_names)
            semester_info.upsert(semester_title, is_publicly_visible)
            if not error:
                return Response(status_code=200)
            return Response(error, status_code=500)
    return Response("Did not receive proper form data", status_code=500)

@app.get('/api/user/course')
async def get_student_courses(request: Request):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    student_courses, error = course_select.get_selection(request.session['user']['user_id'])
    return student_courses if not error else Response(error, status_code=500)


@app.get('/api/user/{session_id}')
async def get_user_info(request: Request, session_id):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.get_user_info(session_id)

@app.post('/api/user')
async def add_user(user: UserPydantic):
    return user_controller.add_user(user.dict())

@app.delete('/api/user')
async def delete_user(request: Request, session: UserDeletePydantic):

    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.delete_user(session.dict())

@app.put('/api/user')
async def update_user_info(request:Request, user:UpdateUser):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.update_user(user)

@app.post('/api/session')
async def log_in(request: Request, credentials: SessionPydantic):
    session_res = session_controller.add_session(credentials.dict())
    if session_res['success']:
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
def add_user_event(_request: Request):# _credentials: SessionPydantic):
    return Response(status_code=501)

@app.post('/api/user/course')
async def add_student_course(request: Request, credentials: UserCoursePydantic):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)
    _resp, error = course_select.add_selection(credentials.name, credentials.semester,
                                               request.session['user']['user_id'], credentials.cid)
    return Response(status_code=200) if not error else Response(error, status_code=500)


@app.delete('/api/user/course')
async def remove_student_course(request: Request, course_delete:CourseDeletePydantic):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)
    _resp,error = course_select.remove_selection(course_delete.name, course_delete.semester,
                                                 request.session['user']['user_id'],
                                                 course_delete.cid)
    return Response(status_code=200) if not error else Response(error, status_code=500)

@app.get('/api/professor/name/{email}')
async def get_professor_name_by_email(email: str):
    # searches professor's first and last name by email
    professor_name, error = professor_info.get_professor_name_by_email(email)
    # Return the data as a JSON response
    return professor_name if not error else Response(content=error, status_code=500)

@app.get('/api/professor/department/{department}')
async def get_professor_from_department(department: str):
    professors, error = professor_info.get_professors_by_department(department)
    return professors if not error else Response(content=error, status_code=500)

@app.get('/api/professor')
@cache(expire=Constants.DAY_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def get_all_professors():
    """
    GET /api/professor
    Cached: 24 Hours
    """
    professors, error = professor_info.get_all_professors() # replace professor_info with db_manager
    db_list = [dict(prof) for prof in professors] if professors else []
    return db_list if not error else Response(error, status_code = 500)

@app.get('/api/professor/phone_number/{email}')
async def get_professor_phone_number_by_email(email: str):
    phone_number, error = professor_info.get_professor_phone_number_by_email(email)
    return phone_number if not error else Response(content=error, status_code=500)


@app.get('/api/professor/email/{email}')
async def get_professor_info_by_email(email:str):
    professor_email, error = professor_info.get_professor_info_by_email(email)
    return professor_email if not error else Response(content=error, status_code=500)

#@app.delete('/api/user/course')
# async def remove_student_course(request: Request, courseDelete:CourseDeletePydantic):
#     if 'user' not in request.session:
#         return Response("Not authorized", status_code=403)
#     resp,error = course_select.remove_selection(courseDelete.name, courseDelete.semester,
#                                                 request.session['user']['user_id'],
#                                                 courseDelete.cid)
#     return Response(status_code=200) if not error else Response(error, status_code=500)

@app.post('/api/professor/add/{msg}')
async def add_professor(msg:str):
    info = msg.split(",")
    #msg should be name, title , email ,phone number, dep, portfolio page, rcs
    # rcs = info[2].split("@")
    # id = rcs[0]
    # print("name", info[0])
    # print("title", info[1])
    # print("email", info[2])
    # print("phone", info[3])
    # print("dep", info[4])
    # print("portfolio_page", info[5])
    # print("rcs", id)

    professor, error = professor_info.add_professor(info[0], info[1], info[2], info[3] , info[4],
    info[5], info[6])
    return professor if not error else Response(error, status_code=500)

@app.post('/api/professor/add/test')
async def add_test_professor():
    professor, error = professor_info.add_professor("random", "person", "number", "test?@rpi.edu",
                                                    "CSCI", "lally 300", "52995")
    return professor if not error else Response(content = error, status_code = 500)

@app.delete('/api/professor/remove/{email}')
async def remove_professor(email:str):
    print(email)
    professor, error = professor_info.remove_professor(email)
    return professor if not error else Response(str(error), status_code=500)

@app.delete('/api/semester/{id}')
async def remove_semester(semester_id: str):
    print(semester_id)
    semester, error = courses.delete_by_semester(semester=semester_id)
    return semester if not error else Response(str(error), status_code=500)

@app.get('/api/getFinalsCRNs')
async def get_finals_crns():
    finals_data = finals_info.get_finals_data()
    return finals_data

@app.get('/api/getFinalDataFromCRN')
async def get_final_data(crn: str):
    return finals_info.get_single_final_data(crn)
