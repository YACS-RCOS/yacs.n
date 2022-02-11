import pytest
from .util import Client

@pytest.fixture(scope="session")
def client():
    return Client()

@pytest.fixture(scope="session")
def upload(client):
    multipart_form_data = (
        ('file', ('test_data.csv', open('tests/test_data.csv', 'rb'))),
        ('isPubliclyVisible', (None, "on")),
    )
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
