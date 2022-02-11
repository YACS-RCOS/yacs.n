from .util import Client
from .fixtures import *

TEST_USER = { 'email': TEST_USER_SIGNUP['email'],
              'password': TEST_USER_SIGNUP['password'] }
TEST_USER_COURSE = {
    "name": "ADMN-1824",
    "semester": "SUMMER 2020",
    "cid": "-1"
}
# TEST_USER_SIGNUP = { 'email': 'test@email.com',
#                      'name': 'TestName',
#                      'phone': '',
#                      'password': '123456',
#                      'degree': 'Undergraduate',
#                      'major': 'CSCI' }
def test_user_course_post_success(post_user, client: Client):
    '''
    Test user course post by comparing it to user course get
    '''
    s = client.post("/api/session", json=TEST_USER)
    assert s.status_code == 200
    r = client.post("/api/user/course", json=TEST_USER_COURSE)
    assert r.status_code == 200
    data = r.json()
    g = client.get("/api/user/course", json=TEST_USER_COURSE)
    get_data = g.json()
    print(get_data)
    assert data['content'] is not None
    assert data['content']['name'] is not None
    assert data['content']['semester'] is not None
    assert data['content']['cid'] is not None

    assert data['content']['name'] == get_data['content']['name']
    assert data['content']['semester'] == get_data['content']['semester']
    assert data['content']['cid'] == get_data['content']['cid']

def test_user_course_post_failure(client: Client):
    '''
    Test user course post with invalid parameter
    '''
    MISMATCH_TEST_USER_COURSE = {
    "name": "AAAAAA",
    "semester": "BBBB",
    "cid": "9999"
    }
    s = client.post("/api/session", json=TEST_USER)
    assert s.status_code == 200
    r = client.post("api/user/course", json=TEST_USER_COURSE)
    assert r.status_code == 200
    data = r.json()
    g = client.get("/api/user/course", json=MISMATCH_TEST_USER_COURSE)
    get_data = g.json()

    assert data['content']['name'] != get_data['content']['name']
    assert data['content']['semester'] != get_data['content']['semester']
    assert data['content']['cid'] != get_data['content']['cid']