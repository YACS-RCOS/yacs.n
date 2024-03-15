from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, UploadFile, Form, File, Depends, Security
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi.security import APIKeyHeader
from fastapi import DependsI
import db.professor as All_professors
import db.connection as connection
from fastapi_cache.backends.inmemory import InMemoryBackend
import db.student_course_selection as CourseSelect
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from constants import Constants
import os
from api_models import *
import controller.user as user_controller

db_conn = connection.db
course_select = CourseSelect.student_course_selection(db_conn)

router = APIRouter(
    prefix='/professors',
    tags=['professors'],
    responses={404: {'description': 'Not found'}}
)

@router.get('/api/user/course')
async def get_student_courses(request: Request):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    courses, error = course_select.get_selection(
        request.session['user']['user_id'])
    return courses if not error else Response(error, status_code=500)


@router.get('/api/user/{session_id}')
async def get_user_info(request: Request, session_id):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.get_user_info(session_id)


@router.post('/api/user')
async def add_user(user: UserPydantic):
    return user_controller.add_user(user.dict())


@router.delete('/api/user')
async def delete_user(request: Request, session: UserDeletePydantic):

    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.delete_user(session.dict())


@router.put('/api/user')
async def update_user_info(request: Request, user: updateUser):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)

    return user_controller.update_user(user)

@router.post('/api/user/course')
async def add_student_course(request: Request, credentials: UserCoursePydantic):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)
    resp, error = course_select.add_selection(
        credentials.name, credentials.semester, request.session['user']['user_id'], credentials.cid)
    return Response(status_code=200) if not error else Response(error, status_code=500)


@router.delete('/api/user/course')
async def remove_student_course(request: Request, courseDelete: CourseDeletePydantic):
    if 'user' not in request.session:
        return Response("Not authorized", status_code=403)
    resp, error = course_select.remove_selection(
        courseDelete.name, courseDelete.semester, request.session['user']['user_id'], courseDelete.cid)
    return Response(status_code=200) if not error else Response(error, status_code=500)
