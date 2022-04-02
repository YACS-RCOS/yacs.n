#from .util import Client
from fastapi.testclient import TestClient
import pytest

TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

TEST_COURSE = {'name': 'ARCH-4770',
               'cid': '-1',
               'semester': 'SUMMER2020'}

@pytest.mark.testclient
@pytest.mark.incompletedependency
def test_user_course_get_success(post_user, client: TestClient):
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    course = client.post("/api/user/course", json=TEST_COURSE)
    assert course.status_code == 200
    d = client.get("/api/user/course", json=TEST_COURSE)
    data = d.json()[1]
    assert data['course_name'] == TEST_COURSE['name']
    assert data['crn'] == TEST_COURSE['cid']
    assert data['semester'] == TEST_COURSE['semester']
    client.delete("/api/session", json = {"sessionID": r.json()["content"]["sessionID"]})

@pytest.mark.testclient
def test_user_course_get_failure(client: TestClient):
    r = client.post("/api/user/course", json = TEST_COURSE)
    assert r.status_code == 403

