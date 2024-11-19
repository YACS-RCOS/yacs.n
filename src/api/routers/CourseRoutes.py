from fastapi import APIRouter, HTTPException, Request, Response, UploadFile, Form, File, Depends, Security
from fastapi.security import APIKeyHeader
import os
from io import StringIO
import pandas as pd
from api_models import *

from db.StudentCourseSelection import StudentCourseSelection
from db.courses import Courses
from db.SemesterInfo import SemesterInfo

api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in os.environ.get("API_SIGN_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=Request.status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


class CourseRoutes:
    
    def __init__(self, db_conn, cache):
        self.courses = Courses(db_conn, cache)
        self.semester_info = SemesterInfo(db_conn, cache)
        self.course_select = StudentCourseSelection(db_conn)
        self.router = APIRouter(
            prefix='/api'
        )
        self.router.add_api_route('/user/course', self.get_courses, methods=['GET'])
        self.router.add_api_route('/bulkCourseUpload', self.upload, methods=['POST'])
        self.router.add_api_route('/user/course', self.add_course, methods=['POST'])
        self.router.add_api_route('/user/course', self.remove_course, methods=['DELETE'])

    # Parses the data from the .csv data files
    async def upload(
            self,
            isPubliclyVisible: str = Form(...),
            file: UploadFile = File(...),
            api_key: str = Security(get_api_key)):
        # check for user files
        print("in process")
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
            self.semester_info.upsert(semester, isPubliclyVisible)
        # Like C, the cursor will be at EOF after full read, so reset to beginning
        csv_file.seek(0)
        # Clear out course data of the same semester before population due to
        # data source (E.g. SIS & Acalog Catalog) possibly updating/removing/adding
        # courses.
        self.courses.bulk_delete(semesters=semesters)
        # Populate DB from CSV
        isSuccess, error = self.courses.populate_from_csv(csv_file)
        if (isSuccess):
            return Response(status_code=200)
        print(error)
        return Response(error.__str__(), status_code=500)


    async def add_course(self, request: Request, credentials: UserCoursePydantic):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)
        resp, error = self.course_select.add_selection(
            credentials.name, credentials.semester, request.session['user']['user_id'], credentials.cid)
        return Response(status_code=200) if not error else Response(error, status_code=500)


    async def remove_course(self, request: Request, courseDelete: CourseDeletePydantic):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)
        resp, error = self.course_select.remove_selection(
            courseDelete.name, courseDelete.semester, request.session['user']['user_id'], courseDelete.cid)
        return Response(status_code=200) if not error else Response(error, status_code=500)


    async def get_courses(self, request: Request):
        if 'user' not in request.session:
            return Response("Not authorized", status_code=403)

        courses, error = self.course_select.get_selection(
            request.session['user']['user_id'])
        return courses if not error else Response(error, status_code=500)
