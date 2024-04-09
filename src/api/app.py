#!/usr/bin/python3
from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, Form, File, Depends, Security
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi.security import APIKeyHeader
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
from sqlalchemy.orm import Session
import json
import os
import pandas as pd
from routers.ProfessorRoutes import ProfessorRoutes
from routers.CourseRoutes import CourseRoutes
from routers.UserRoutes import UserRoutes
from constants import Constants

"""
NOTE: on caching
on add of semester of change of data from GET
do a cache.clear() to ensure data integrity
"""

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=os.environ.get("API_SIGN_KEY", "localTestingKey"))
FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
api_key_header = APIKeyHeader(name="X-API-Key")


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in os.environ.get("API_SIGN_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=Request.status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


# - init interfaces to db
db_conn = connection.db
class_info = ClassInfo.ClassInfo(db_conn)
date_range_map = DateMapping.semester_date_mapping(db_conn)
admin_info = AdminInfo.Admin(db_conn)
semester_info = SemesterInfo.semester_info(db_conn, FastAPICache)
users = UserModel.User()
professor_routes = ProfessorRoutes(db_conn, FastAPICache)
user_routes = UserRoutes()
course_routes = CourseRoutes()


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


@app.get("/api/auth")
async def authenticate(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}


@app.get('/api/class')
@cache(expire=Constants.HOUR_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def get_classes(request: Request, semester: str = None, search: str = None):
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
        if search:
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

@app.delete('/api/semester/{semester_id}')
async def remove_semester(semester_id: str, api_key: str = Security(get_api_key)):
    print(semester_id)
    semester, error = semester_info.delete_semester(semester=semester_id)
    return semester if not error else Response(str(error), status_code=500)

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
def set_defaultSemester(semester_set: DefaultSemesterSetPydantic, api_key: str = Security(get_api_key)):
    success, error = admin_info.set_semester_default(semester_set.default)
    if success:
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
            _, error = date_range_map.insert_all(
                start_dates, end_dates, semester_part_names)
            semester_info.upsert(semester_title, is_publicly_visible)
            if (not error):
                return Response(status_code=200)
            else:
                return Response(error, status_code=500)
    return Response("Did not receive proper form data", status_code=500)


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


# add support for finals schedule/endpoints
app.include_router(professor_routes.router)
app.include_router(course_routes.router)
app.include_router(user_routes.router)