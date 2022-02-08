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
