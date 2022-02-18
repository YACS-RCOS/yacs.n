import pytest
from fastapi.testclient import TestClient
import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
appdir = os.environ.get("TEST_APP_DIR", parentdir)
sys.path.insert(0, appdir)

from app import app
from db.connection import db
from tables.database_session import SessionLocal, DB_PASS

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "testclient: mark tests that are updated to use FastAPI's TestClient"
    )

### Create the database session and clear tables needed for testing
session = SessionLocal()
cur = db.get_connection().cursor()
cur.execute(" DELETE FROM public.user_account ")    # Remove users
cur.execute(" DELETE FROM course_session ")         # Remove course data
cur.execute(" DELETE FROM public.user_session ")    # Removes outstanding sessions
cur.close()

@pytest.fixture(scope="session")
def client():
    yield TestClient(app)

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
