from fastapi import APIRouter, FastAPI, HTTPException, Request, Response, UploadFile, Form, File, Depends, Security
from starlette.middleware.sessions import SessionMiddleware
from fastapi_cache import FastAPICache
from fastapi.security import APIKeyHeader
from fastapi import DependsI
import db.professor as All_professors
import db.connection as connection
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from constants import Constants
import os

db_conn = connection.db
professor_info = All_professors.Professor(db_conn, FastAPICache)
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in os.environ.get("API_SIGN_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=Request.status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

router = APIRouter(
    prefix='/professors',
    tags=['professors'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/')
@cache(expire=Constants.DAY_IN_SECONDS, coder=PickleCoder, namespace="API_CACHE")
async def get_all_professors(): 
    """
    GET /api/professor
    Cached: 24 Hours
    """
    professors, error = professor_info.get_all_professors(
    )  # replace professor_info with db_manager
    db_list = [dict(prof) for prof in professors] if professors else []
    return db_list if not error else Response(error, status_code=500)


@router.get('/email/{email}')
async def get_professor_info_by_email(email: str):
    professor_email, error = professor_info.get_professor_info_by_email(email)
    return professor_email if not error else Response(content=error, status_code=500)


@router.get('/name/{email}')
async def get_professor_name_by_email(email: str):
    # searches professor's first and last name by email
    professorName, error = professor_info.get_professor_name_by_email(email)
    # Return the data as a JSON response
    return professorName if not error else Response(content=error, status_code=500)


@router.get('/department/{department}')
async def get_professor_from_department(department: str):
    professors, error = professor_info.get_professors_by_department(department)
    return professors if not error else Response(content=error, status_code=500)


@router.get('/phone_number/{email}')
async def get_professor_phone_number_by_email(email: str):

    phone_number, error = professor_info.get_professor_phone_number_by_email(email)
    return phone_number if not error else Response(content=error, status_code=500)


@router.post('/add/{msg}')
async def add_professor(msg: str, api_key: str = Security(get_api_key)):
    info = msg.split(",")
    professor, error = professor_info.add_professor(info[0], info[1], info[2], info[3], info[4],
                                                    info[5], info[6], info[7], info[8])
    return professor if not error else Response(error, status_code=500)


@router.delete('/remove/{email}')
async def remove_professor(email: str, api_key: str = Security(get_api_key)):
    print(email)
    professor, error = professor_info.remove_professor(email)
    return professor if not error else Response(str(error), status_code=500)
