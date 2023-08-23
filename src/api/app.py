#!/usr/bin/python3
from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, Form, File, Depends, Body
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from typing import Dict, Optional
import asyncio
import random
import time
import uuid
import hashlib

from api_models import *
import db.connection as connection
import db.classinfo as ClassInfo
import db.courses as Courses
import db.professor as All_professors
import db.semester_info as SemesterInfo
import db.semester_date_mapping as DateMapping
import db.admin as AdminInfo
import db.student_course_selection as CourseSelect
import db.user as UserModel
import db.dp_schedules as DpSchedules

from degree_planner.planner import Planner
from degree_planner.math.dictionary_array import Dict_Array
from degree_planner.dp.requirement import Requirement
from degree_planner.user.schedule import Schedule

from redis_manipulations import get_redis_status, purify, get_schedule, save_schedule, delete_schedule

import controller.user as user_controller
import controller.session as session_controller
import controller.userevent as event_controller
from io import StringIO
from sqlalchemy.orm import Session
import os
import pandas as pd
import copy
from constants import Constants

from celery_app import dp_recommend, dp_fulfill, dp_fulfill_groups, dp_fulfill_details

"""
NOTE: on caching
on add of semester of change of data from GET
do a cache.clear() to ensure data integrity
"""

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=os.environ.get("API_SIGN_KEY", "localTestingKey"))

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
courses = Courses.Courses(db_conn, FastAPICache)
date_range_map = DateMapping.semester_date_mapping(db_conn)
admin_info = AdminInfo.Admin(db_conn)
course_select = CourseSelect.student_course_selection(db_conn)
semester_info = SemesterInfo.semester_info(db_conn)
professor_info =  All_professors.Professor(db_conn, FastAPICache)
users = UserModel.User()
dp_schedules = DpSchedules.Dp_schedules(db_conn)

planner = Planner(enable_tensorflow=False)
planner.import_data()

hash_heads = set()
hash_heads_queue = []
MAX_HASH_HEADS = 10000
difficulty = '000'

recommendation_results = dict() # {user: results}
fulfillment_detail_results = dict() # {user: details}

def rate_limited(seconds_interval):
    def decorator(func):
        call_history = {}
        add_history = {}
        async def rate_limited_function(userid, *args, **kwargs):
            time_added = time.time()
            add_history.update({userid:time_added})
            time_elapsed = time.time() - call_history.get(userid, 0.0)
            time_wait = seconds_interval - time_elapsed

            debug_time = time.time()

            if time_wait > 0:
                print(f'rate limited!')
                await asyncio.sleep(time_wait)

            if add_history.get(userid) != time_added:
                # means another call occurred while waiting, so cancel this one
                print(f'cancelling function call sent at time {debug_time}')
                return

            print(f'executing function call made at time {debug_time}')
            
            call_history.update({userid:time.time()})
            return await func(userid, *args, **kwargs)
        return rate_limited_function
    return decorator

def is_admin_user(session):
    if 'user' in session and (session['user']['admin'] or session['user']['super_admin']):
        return True
    return False



##########################################################################
##########################################################################
'''=======================DELETE BEFORE MERGING========================'''

@app.get('/api/dp/redisstat')
async def dp_redis_status():
    return get_redis_status()

@app.get('/api/dp/redispurify')
async def dp_redis_purify():
    await purify()

'''===================================================================='''
##########################################################################
##########################################################################



async def dp_redis_delete_schedule(scheduleid):
    await delete_schedule(scheduleid)

@app.get("/api/dp/newuser")
async def dp_new_user():
    # Generate a token and userid
    global hash_heads
    global hash_heads_queue

    hashhead = str(uuid.uuid4())
    while hashhead in hash_heads:
        print(f'AN ASTRONOMICALLY UNLIKELY EVENT HAS OCCURRED (uuid4 collision)')
        hashhead = str(uuid.uuid4())
    hash_heads.add(hashhead)
    hash_heads_queue.append(hashhead)

    if len(hash_heads_queue) > MAX_HASH_HEADS:
        for discardedHash in hash_heads_queue[:int(MAX_HASH_HEADS / 2)]:
            hash_heads.remove(discardedHash)
        hash_heads_queue = hash_heads_queue[int(MAX_HASH_HEADS / 2):]
    global difficulty
    # print(f'beginning new session with hashhead {hashhead}')
    return {'hashhead': hashhead, 'difficulty': difficulty}

# a dead simple rate limiter that will probably give a security analyst a stroke
def valid_hash(hashval:str):
    if len(hashval) < 36:
        return False
    if hashval[0:36] not in hash_heads:
        return False

    input_bytes = hashval.encode('utf-8')
    return (hashlib.sha256(input_bytes).hexdigest()[0:len(difficulty)] == difficulty)

@app.get("/api/dp/validateid/{userid}")
async def dp_validate_id(userid:str):
    print(f'user attempted to validate id {userid}: {valid_hash(userid)}! current valid heads: {hash_heads}')
    return {'valid': valid_hash(userid)}

@app.get('/api/dp/info')
async def dp_info():
    return {"degrees":planner.degrees()}

@app.get('/api/dp/getschedule/{scheduleid}')
async def dp_get_schedule(scheduleid:str):
    # dictionary of schedule data
    schedule_data = await get_schedule(scheduleid)
    return schedule_data

@app.post('api/dp/saveschedule')
async def dp_save_schedule(schedule_data:dict = Body(...)):
    # verify schedule_data structure: {'name':schedule_name, 'courses':course_names, 'degree':degree_name}
    if not len(schedule_data) == 3:
        return False
    if not isinstance(str, schedule_data.get('name', None)):
        return False
    if not isinstance(list, schedule_data.get('courses', None)):
        return False
    for course in schedule_data.get('courses'):
        if not isinstance(str, course):
            return False
    if not isinstance(str, schedule_data.get('degree', None)):
        return False
    
    save_schedule(schedule_data.get('name'), schedule_data)

@app.post('/api/dp/fulfillment')
async def dp_get_fulfillment(userid:str = Body(...), degree_name:str = Body(...), taken_courses:list = Body(...), attributes_replacement:dict = Body(...)):
    if not valid_hash(userid):
        return None
    
    io = planner.output

    wildcard_resolutions = Dict_Array(attributes_replacement, list_type='list')
    degree = planner.get_degree(degree_name)
    if degree is None:
        return None
    
    requirements = degree.requirements
    groups = degree.groups

    taken_courses_convert_to_elements = []
    for course in taken_courses:
        element = planner.catalog.get_element(course)
        if element is None:
            continue
        taken_courses_convert_to_elements.append(element)
    taken_courses = taken_courses_convert_to_elements
    templates = planner.catalog.get_templates()

    fulfillment = dp_fulfill(taken_courses, requirements, wildcard_resolutions, groups, False, templates)
    formatted_fulfillments = io.format_fulfillments_dict(fulfillment, taken_courses)

    # BEGIN DETAILS COMPUTATION ----
    await dp_begin_fulfillment_details(userid, taken_courses, planner.catalog, requirements, wildcard_resolutions)
    #-------------------------------

    fulfillment_groups_and_tally = dp_fulfill_groups(fulfillment, groups) # contains groups and tally
    fulfillment_groups_and_tally.update({'groups': io.format_fulfillment_groups(fulfillment_groups_and_tally.get('groups'))}) # formats groups
    fulfillment_groups_and_tally.update({'fulfillments': formatted_fulfillments}) # adds fulfillments

    return fulfillment_groups_and_tally

@rate_limited(3)
async def dp_begin_fulfillment_details(userid:str, taken_courses, catalog, requirements, wildcard_resolutions):
    details = dp_fulfill_details.delay(taken_courses, catalog, requirements, wildcard_resolutions)
    fulfillment_detail_results.update({userid:details})


@app.get('/api/dp/fulfillmentdetails/{userid}')
async def dp_get_fulfillment_details(userid:str):
    if not valid_hash(userid):
        return None
    
    i = 0
    while(fulfillment_detail_results.get(userid, None) is None or not fulfillment_detail_results.get(userid).ready()):
        await asyncio.sleep(1)
        print(f'waiting for fulfillment details...  queued: {fulfillment_detail_results.get(userid, None) is not None}')
        if fulfillment_detail_results.get(userid, None) is None:
            return None
        i+=1
        if i > 20:
            print('timeout')
            return None
    
    details = fulfillment_detail_results.get(userid).result
    return details

@rate_limited(3)
async def dp_begin_recommendation_limited(userid:str, degree_name:str, taken_courses:list, attributes_replacement:dict):
    degree = planner.get_degree(degree_name)
    if degree is None:
        return
    requirements = degree.requirements
    wildcard_resolutions = Dict_Array(attributes_replacement, list_type='list')

    taken_courses_convert_to_elements = []
    for course in taken_courses:
        element = planner.catalog.get_element(course)
        if element is None:
            continue
        taken_courses_convert_to_elements.append(element)
    taken_courses = taken_courses_convert_to_elements

    recommendation = dp_recommend.delay(taken_courses, planner.catalog, requirements, specification_sets=Requirement.specification_sets, attributes_replacement=wildcard_resolutions)
    recommendation_results.update({userid:recommendation})
    
@app.post('/api/dp/recommend')
async def dp_begin_recommendation(userid:str = Body(...), degree_name:str = Body(...), taken_courses:list = Body(...), attributes_replacement:dict = Body(...)):
    if not valid_hash(userid):
        return
    await dp_begin_recommendation_limited(userid, degree_name, taken_courses, attributes_replacement)

@app.get('/api/dp/recommend/{userid}')
async def dp_get_recommendation(userid:str):
    if not valid_hash(userid):
        return None
    
    io = planner.output
    i = 0
    while(recommendation_results.get(userid, None) is None or not recommendation_results.get(userid).ready()):
        await asyncio.sleep(1)
        print(f'waiting for recommendation...  queued: {recommendation_results.get(userid, None) is not None}')
        if recommendation_results.get(userid, None) is None:
            return None
        i+=1
        if i > 40:
            print('timeout')
            return None
    
    recommendation = recommendation_results.get(userid).result
    formatted_recommendations = io.format_recommendations(recommendation)
    #print(f'RECOMMENDATIONS: {formatted_recommendations}')
    results = Dict_Array(list_type='list')

    # formatted recommendations is a list of dictionaries with each dictionary being a recommendation, containing
    # entries such as name and fulfillment set
    for recommendation in formatted_recommendations:
        results.add(recommendation['name'], recommendation)

    results.sort_elements('get', ("courses_fulfilled",), True)
    return results.dictionary

@app.get('/api/dp/courses/{lowercase}')
async def dp_get_courses(lowercase:bool):
    courses = list(planner.catalog.get_elements())
    if lowercase:
        courses = [course.name.casefold() for course in courses]
    else:
        courses = [course.name for course in courses]
    courses.sort()
    return courses

@app.get('/api/dp/subjectgroups')
async def dp_get_subject_groups():
    return planner.subject_groups

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
    print(semester)
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

@app.get('/api/user/course')
async def get_student_courses(request: Request):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    courses, error = course_select.get_selection(request.session['user']['user_id'])
    return courses if not error else Response(error, status_code=500)


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
    return Response(status_code=200) if not error else Response(error, status_code=500)

@app.get('/api/professor/name/{email}')
async def get_professor_name_by_email(email: str):
    # searches professor's first and last name by email
    professorName, error = professor_info.get_professor_name_by_email(email)
    # Return the data as a JSON response
    return professorName if not error else Response(content=error, status_code=500)

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
    professors, error = professor_info.get_all_professors()  # replace professor_info with db_manager
    db_list = [dict(prof) for prof in professors] if professors else []
    return db_list if not error else Response(error, status_code = 500)

@app.get('/api/professor/office_hours/{email}')
async def get_office_hours(email: str):
    professor_office_hours, error = professor_info.get_office_hours_by_email(email)    
    return professor_office_hours if not error else Response(content=error, status_code=500)

@app.get('/api/professor/phone_number/{email}')
async def get_professor_phone_number_by_email(email: str):
    phone_number, error = professor_info.get_professor_phone_number_by_email(email)
    return phone_number if not error else Response(content=error, status_code=500)

@app.get('/api/professor/rcs/{rcs}')
async def get_professor_info_by_rcs(rcs:str):
    professor_rcs, error = professor_info.get_professor_info_by_rcs(rcs)
    return professor_rcs if not error else Response(content=error,status_code=500)

@app.get('/api/professor/email/{email}')
async def get_professor_info_by_email(email:str):
    professor_email, error = professor_info.get_professor_info_by_email(email)
    return professor_email if not error else Response(content=error, status_code=500)

#@app.delete('/api/user/course')
# async def remove_student_course(request: Request, courseDelete:CourseDeletePydantic):
#     if 'user' not in request.session:
#         return Response("Not authorized", status_code=403)
#     resp,error = course_select.remove_selection(courseDelete.name, courseDelete.semester, request.session['user']['user_id'], courseDelete.cid)
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
    info[5], info[6], info[7], info[8])
    return professor if not error else Response(error, status_code=500)

@app.post('/api/professor/add/test')
async def add_test_professor():
    professor, error = professor_info.add_professor("random", "person", "number", "test?@rpi.edu", "CSCI", 
        "lally 300", "52995")
    return professor if not error else Response(content = error, status_code = 500)

@app.delete('/api/professor/remove/{email}')
async def remove_professor(email:str):
    print(email)
    professor, error = professor_info.remove_professor(email)
    return professor if not error else Response(str(error), status_code=500)

#Parses the data from the .csv data files
@app.post('/api/bulkProfUpload')
async def uploadHandler(file: UploadFile = File(...)):
    # check for user files
    if not file:
        return Response("No file received", 400)
    if file.filename.find('.') == -1 or file.filename.rsplit('.', 1)[1].lower() != 'csv':
        return Response("File must have csv extension", 400)
    # get file
    contents = await file.read()
    csv_file = StringIO(contents.decode())
    isSuccess, error = courses.populate_from_csv(csv_file)
    # Populate DB from CSV
    if (isSuccess):
        return Response(status_code=200)
    else:
        print(error)
        return Response(error.__str__(), status_code=500)
