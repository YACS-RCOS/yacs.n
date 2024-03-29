from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, UploadFile, Form, File, Depends, Security
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi.security import APIKeyHeader
import db.professor as All_professors
import db.connection as connection
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from constants import Constants
import os
import json

class Professors:
    
    def __init__(self, professor_info):
        self.professor_info = professor_info
        self.router = APIRouter(
            prefix='/api/professor'
        )
        self.router.add_api_route('', self.get_professors, methods=['GET'])
        self.router.add_api_route('', self.upload_professors, methods=['POST'])

    @cache(expire=Constants.DAY_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
    async def get_professors(self):
        """
        GET /api/professor
        Cached: 24 Hours
        """
        professors, error = self.professor_info.get_all_professors(
        )  # replace professor_info with db_manager
        db_list = [dict(prof) for prof in professors] if professors else []
        return db_list if not error else Response(error, status_code=500)
    
    async def upload_professors(
            self,
            isPubliclyVisible: str = Form(...),
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
            # convert string to python dict
            json_data = json.loads(contents.decode('utf-8'))
            # print(json_data)
        except json.JSONDecodeError as e:
            return Response(f"Invalid JSON data: {str(e)}", 400)

        # Call populate_from_json method
        isSuccess, error = self.professor_info.populate_from_json(json_data)
        if isSuccess:
            print("SUCCESS")
            return Response(status_code=200)
        else:
            print("NOT WORKING")
            print(error)
            return Response(error.__str__(), status_code=500)
