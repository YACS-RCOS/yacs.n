from fastapi.testclient import TestClient
import pytest

TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

TEST_USER_COURSE = {'name': 'ADMN-1824',
                    'semester': 'SUMMER 2020',
                    'cid': '-1'
}

'''
Test this api endpoint/file locally with the following command line:
src/api/tests/test.sh
'''
@pytest.mark.testclient
@pytest.mark.incompletedependency
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
    print(r.text)
    assert r.status_code == 403
