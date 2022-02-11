from .util import Client
from .fixtures import *

TEST_USER = { 'email': TEST_USER_SIGNUP['email'],
              'password': TEST_USER_SIGNUP['password'] }

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

    r = client.post("/api/user/course", json={
            "name": "ADMN-1824",
            "semester": "SUMMER 2020",
            "cid": "-1"
            })
    assert r.status_code == 200
    data = r.json()
    g = client.get("/api/user/course", json=TEST_USER)
    get_data = g.json()
    print(get_data)
    assert data['content'] is not None
    assert data['content']['course_name'] is not None
    assert data['content']['crn'] is not None
    assert data['content']['semester'] is not None

    assert data['content']['course_name'] == get_data['content']['course_name']

def test_user_course_post_failure(client: Client):
    '''
    Test user course post with invalid credentials
    '''
    # r = client.post("/api/user/course", json={'name':'NotAUser', 'password':'000000'})
    # assert r.status_code == 200

    # data = r.json()
    # assert data['content'] is None
