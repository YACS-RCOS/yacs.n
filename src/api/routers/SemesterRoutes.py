from fastapi import APIRouter, HTTPException, Request, Response, Security
from fastapi.security import APIKeyHeader
import os
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from api_models import *
from constants import Constants


from db.SemesterInfo import SemesterInfo

import db.semester_date_mapping as DateMapping

from db.classinfo import ClassInfo


api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in os.environ.get("API_SIGN_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=Request.status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


def is_admin_user(session):
    if 'user' in session and (session['user']['admin'] or session['user']['super_admin']):
        return True
    return False


class SemesterRoutes:
    
    def __init__(self, db_conn, cache):
        self.class_info = ClassInfo(db_conn)
        self.semester_info = SemesterInfo(db_conn, cache)
        self.date_range_map = DateMapping.semester_date_mapping(db_conn)
        self.router = APIRouter(
            prefix='/api'
        )
        self.router.add_api_route('/class', self.get_classes, methods=['GET'])
        self.router.add_api_route('/semester', self.remove_semester, methods=['DELETE'])


    @cache(expire=Constants.HOUR_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
    async def get_classes(self, request: Request, semester: str = None, search: str = None):
        """
        GET /api/class?semester={}&search={}
        Cached: 1 Hour
        """
        if semester:
            if not self.semester_info.is_public(semester):
                if is_admin_user(request.session):
                    classes, error = self.class_info.get_classes_full(semester)
                    return classes if not error else Response(error, status_code=500)
                return Response(content="Semester isn't available", status_code=401)
            if search:
                classes, error = self.class_info.get_classes_by_search(semester, search)
            else:
                classes, error = self.class_info.get_classes_full(semester)
            return classes if not error else Response(error, status_code=500)
        return Response(content="missing semester option", status_code=400)


    #@app.delete('/api/semester/{semester_id}')
    async def remove_semester(self, semester_id: str, api_key: str = Security(get_api_key)):
        print(semester_id)
        semester, error = self.semester_info.delete_semester(semester=semester_id)
        return semester if not error else Response(str(error), status_code=500)

    #@app.get('/api/semesterInfo')
    def get_all_semester_info(self):
        all_semester_info, error = self.class_info.get_all_semester_info()
        return all_semester_info if not error else Response(error, status=500)

    #@app.post('/api/mapDateRangeToSemesterPart')
    async def map_date_range_to_semester_part_handler(self, request: Request):
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
                _, error = self.date_range_map.insert_all(
                    start_dates, end_dates, semester_part_names)
                self.semester_info.upsert(semester_title, is_publicly_visible)
                if (not error):
                    return Response(status_code=200)
                else:
                    return Response(error, status_code=500)
        return Response("Did not receive proper form data", status_code=500)

