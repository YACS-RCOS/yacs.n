from fastapi import APIRouter, HTTPException, Response, Request, UploadFile, Form, File, Security
from db.professor import Professor
from fastapi.security import APIKeyHeader
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from constants import Constants
import json, os

api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in os.environ.get("API_SIGN_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=Request.status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

class ProfessorRoutes:
    
    def __init__(self, db_conn, cache):
        self.professor_info = Professor(db_conn, cache)
        self.router = APIRouter(
            prefix='/api'
        )
        self.router.add_api_route('/bulkProfessorUpload', self.upload, methods=['POST'])
        self.router.add_api_route('/professor/add/{msg}', self.add, methods=['POST'])
        self.router.add_api_route('/professor', self.get_all, methods=['GET'])
        self.router.add_api_route('/professor/email/{email}', self.get, methods=['GET'])
        self.router.add_api_route('/professor/department/{department}', self.get_department, methods=['GET'])
        self.router.add_api_route('/professor/remove/{email}', self.remove, methods=['DELETE'])

    async def upload(
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


    async def add(self, msg: str, api_key: str = Security(get_api_key)):
        info = msg.split(",")
        professor, error = self.professor_info.add_professor(info[0], info[1], info[2], info[3], info[4],
                                                        info[5], info[6], info[7], info[8])
        return professor if not error else Response(error, status_code=500)


    @cache(expire=Constants.DAY_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
    async def get_all(self):
        """
        GET /api/professor
        Cached: 24 Hours
        """
        professors, error = self.professor_info.get_all_professors(
        )  # replace professor_info with db_manager
        db_list = [dict(prof) for prof in professors] if professors else []
        return db_list if not error else Response(error, status_code=500)
    

    async def get(self, email: str):
        professor_email, error = self.professor_info.get_professor_info_by_email(email)
        return professor_email if not error else Response(content=error, status_code=500)
    

    async def get_department(self, department: str):
        professors, error = self.professor_info.get_professors_by_department(department)
        return professors if not error else Response(content=error, status_code=500)


    async def remove(self, email: str, api_key: str = Security(get_api_key)):
        print(email)
        professor, error = self.professor_info.remove_professor(email)
        return professor if not error else Response(str(error), status_code=500)