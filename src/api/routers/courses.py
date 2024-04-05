from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, UploadFile, Form, File, Depends, Security
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi.security import APIKeyHeader
from fastapi import DependsI
import db.user as User
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

class Courses:
    
    def __init__(self):
        self.router = APIRouter(
            prefix='/api/course'
        )
        self.router.add_api_route('', self.get_student_courses, methods=['GET'])
        self.router.add_api_route('', self.add_student_course, methods=['POST'])
        self.router.add_api_route('', self.remove_student_course, methods=['DELETE'])

    
    async def add_student_course(request: Request, credentials: UserCoursePydantic):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)
        resp, error = course_select.add_selection(
            credentials.name, credentials.semester, request.session['user']['user_id'], credentials.cid)
        return Response(status_code=200) if not error else Response(error, status_code=500)


    async def remove_student_course(request: Request, courseDelete: CourseDeletePydantic):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)
        resp, error = course_select.remove_selection(
            courseDelete.name, courseDelete.semester, request.session['user']['user_id'], courseDelete.cid)
        return Response(status_code=200) if not error else Response(error, status_code=500)


    async def get_student_courses(request: Request):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)

        courses, error = course_select.get_selection(
            request.session['user']['user_id'])
        return courses if not error else Response(error, status_code=500)
