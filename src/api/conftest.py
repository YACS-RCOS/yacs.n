import sys
import os
import inspect
import pytest
from fastapi.testclient import TestClient
from app import app
from tables.database_session import SessionLocal
from tables import Base

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
appdir = os.environ.get("TEST_APP_DIR", parentdir)
sys.path.insert(0, appdir)

### Create the database session and clear tables needed for testing
session = SessionLocal()

for table in reversed(Base.metadata.sorted_tables):
    session.execute(table.delete())
session.commit()

@pytest.fixture(scope="session")
def client():
    yield TestClient(app)

@pytest.fixture(scope="session")
def upload(client_in):
    multipart_form_data = {
        'file': ('test_data.csv', open(appdir + '/tests/test_data.csv', 'rb')),
        'is_publicly_visible': (None, "on"),
    }
    return client_in.post("/api/bulkCourseUpload",
                       files=multipart_form_data)

TEST_USER_SIGNUP = { 'email': 'test@email.com',
                     'name': 'TestName',
                     'phone': '',
                     'password': '123456',
                     'degree': 'Undergraduate',
                     'major': 'CSCI' }

@pytest.fixture(scope="session")
def post_user(client_in):
    return client_in.post('/api/user', json=TEST_USER_SIGNUP)
