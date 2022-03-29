import pytest
from fastapi.testclient import TestClient
from tortoise import run_async
import sys, os, inspect
from typing import Generator

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
appdir = os.environ.get("TEST_APP_DIR", parentdir)
sys.path.insert(0, appdir)

from app import app
from models import UserAccount


async def clear_tables():
    await UserAccount.all().delete()

run_async(clear_tables())

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()

@pytest.fixture(scope="session")
def upload(client):
    multipart_form_data = {
        'file': ('test_data.csv', open(appdir + '/tests/test_data.csv', 'rb')),
        'isPubliclyVisible': (None, "on"),
    }
    return client.post("/api/bulkCourseUpload",
                       files=multipart_form_data)

TEST_USER_SIGNUP = { 'email': 'test@email.com',
                     'name': 'TestName',
                     'phone': '',
                     'password': '123456',
                     'degree': 'Undergraduate',
                     'major': 'CSCI' }

@pytest.fixture(scope="session")
def post_user(client):
    return client.post('/api/user', json=TEST_USER_SIGNUP)
