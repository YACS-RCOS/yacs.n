from .util import Client

TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

TEST_USER_COURSE = {'name': 'ADMN-1824',
                    'semester': 'SUMMER 2020',
                    'cid': '-1'
}

'''
Test this api endpoint/file only with the following command line:
pytest -s tests/test_user_course.py
'''
def test_user_course_post_success(post_user, client: Client):
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

def test_user_course_post_failure(client: Client):
    '''
    Test user course post with invalid parameter
    '''
    TEST_INVALID_USER_COURSE = {}
    sess = client.post("/api/session", json=TEST_USER).json()
    sessID = sess['content']['sessionID']
    r = client.post("/api/user/course", json=TEST_INVALID_USER_COURSE)
    assert r.status_code == 500
    d = client.delete('/api/session', json={'sessionID': sessID})
    assert d.status_code == 200

def test_course_post_not_authorized(client: Client):
    '''
    Test user course post without user session/login
    '''
    r = client.post("/api/user/course", json=TEST_USER_COURSE)
    assert r.status_code == 403