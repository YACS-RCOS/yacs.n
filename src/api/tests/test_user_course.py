from fastapi.testclient import TestClient
import pytest

TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

TEST_USER_COURSE = {'name': 'ADMN-1824',
                    'semester': 'SUMMER 2020',
                    'cid': '-1'}

TEST_COURSE = {'name': 'ARCH-4770',
               'cid': '-1',
               'semester': 'SUMMER2020'}

TEST_COURSE_2 = {'name': 'ARCH-4770',
               'cid': None,
               'semester': 'SUMMER2020'}


@pytest.mark.testclient
def test_user_course_post_success(post_user, client: TestClient):
    '''
    Test user course post by comparing it to user get course
    '''
    sess = client.post("/api/session", json=TEST_USER)
    assert sess.status_code == 200
    r = client.post("/api/user/course", json=TEST_USER_COURSE)
    assert r.status_code == 200
    g = client.get("/api/user/course", json=TEST_USER_COURSE)
    get_data = g.json()[0]
    assert get_data['course_name'] == TEST_USER_COURSE['name']
    assert get_data['semester'] == TEST_USER_COURSE['semester']
    assert get_data['crn'] == TEST_USER_COURSE['cid']
    d = client.delete("/api/session", json={"sessionID": sess.json()['content']['sessionID']})
    assert d.status_code == 200

@pytest.mark.testclient
def test_user_course_post_failure(post_user, client: TestClient):
    '''
    Test user course post with invalid parameter
    '''
    TEST_INVALID_USER_COURSE = {}
    sess = client.post("/api/session", json=TEST_USER).json()
    sessID = sess['content']['sessionID']
    r = client.post("/api/user/course", json=TEST_INVALID_USER_COURSE)
    assert r.status_code == 422
    d = client.delete('/api/session', json={'sessionID': sessID})
    assert d.status_code == 200

@pytest.mark.testclient
def test_course_post_not_authorized(client: TestClient):
    '''
    Test user course post without user session/login
    '''
    sess = client.post("/api/session", json=TEST_USER).json()
    client.delete("/api/session", json={'sessionID': sess['content']['sessionID']})
    r = client.post("/api/user/course", json=TEST_USER_COURSE)
    assert r.status_code == 403

@pytest.mark.testclient
def test_user_course_get_success(post_user, client: TestClient):
    '''
    Test user course get success
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    course = client.post("/api/user/course", json=TEST_USER_COURSE)
    assert course.status_code == 200
    d = client.get("/api/user/course", json=TEST_USER_COURSE)
    data = d.json()[0]
    assert data['course_name'] == TEST_USER_COURSE['name']
    assert data['crn'] == TEST_USER_COURSE['cid']
    assert data['semester'] == TEST_USER_COURSE['semester']
    client.delete("/api/session", json = {"sessionID": r.json()["content"]["sessionID"]})

@pytest.mark.testclient
def test_user_course_get_failure(client: TestClient):
    '''
    Test user course get without user session/login
    '''
    r = client.get("/api/user/course", json = TEST_USER_COURSE)
    assert r.status_code == 403

@pytest.mark.testclient
def test_user_course_delete_success(post_user, client: TestClient):
    '''
    Test user/course delete success
    '''
    l = client.post("/api/session", json=TEST_USER)
    assert l.status_code == 200
    r = client.post("/api/user/course", json=TEST_COURSE)
    assert r.status_code == 200
    r = client.get("/api/user/course")
    assert r.status_code == 200
    data = r.json()
    db_course = {'course_name': TEST_COURSE['name'], 'crn': TEST_COURSE['cid'], 'semester': TEST_COURSE['semester']}
    assert db_course in data

    x = client.delete("/api/user/course", json = TEST_COURSE)
    assert x.status_code == 200
    r = client.get("/api/user/course", json=TEST_COURSE)
    data = r.json()
    assert db_course not in data
    client.delete("/api/session", json = {"sessionID": l.json()["content"]["sessionID"]})

@pytest.mark.testclient
def test_user_course_delete_failure(client: TestClient):
    '''
    Test user course delete with wrong type
    Test user course delete without session/login
    '''
    l = client.post("/api/session", json=TEST_USER)
    r = client.delete("/api/user/course", json={})
    assert r.status_code == 422
    client.delete("/api/session", json = {"sessionID": l.json()["content"]["sessionID"]})
    r = client.delete("/api/user/course", json=TEST_COURSE)
    assert r.status_code == 403
