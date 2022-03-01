from urllib import response
from .util import Client


TEST_USER = { 'email': "test@email.com",
              'password': "123456" }



TEST_USER_SIGNUP = { 'email': 'test@email.com',
                     'name': 'TestName',
                     'phone': '',
                     'password': '123456',
                     'degree': 'Undergraduate',
                     'major': 'CSCI' }


TEST_USER2 = { 'email': "test2@email.com",
              'password': "1234567" }


TEST_USER_SIGNUP2 = { 'email': 'test2@email.com',
                     'name': 'TestName2',
                     'phone': '',
                     'newPassword': '1234567',
                     'degree': 'Graduate',
                     'major': 'ECON' }


'''
Test this api endpoint/file only with the following command line:
pytest -s tests/test_user_course.py
'''

def test_get_user_success(client: Client, post_user):
    '''
    Test user get by using /api/session and TEST_USER_SIGNUP.
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    sessionid = data['content']['sessionID']
    r = client.get("/api/user/"+data['content']['sessionID'])
    assert r.status_code == 200
    data = r.json()
    assert data['content']['degree'] == TEST_USER_SIGNUP['degree']
    assert data['content']['email'] == TEST_USER_SIGNUP['email']
    assert data['content']['major'] == TEST_USER_SIGNUP['major']
    assert data['content']['name'] == TEST_USER_SIGNUP['name']
    assert data['content']['phone'] == TEST_USER_SIGNUP['phone']
    assert data['content']['uid'] is not None
    client.delete("/api/session", {'sessionID': sessionid})

def test_get_user_failed(client: Client,post_user):
    '''
    Test user get with invalid sessionID
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200

    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    '''
    {degree: "Undergraduate", email: "test@email.com", major: "CSCI", name: "TestName", phone: "", uid: 1}
    '''
    r = client.get("/api/user/"+"00000000")
    assert r.status_code == 200
    data = r.json()
    assert data['errMsg'] == "Unable to find the session."


def test_get_user_after_session_closed(client: Client,post_user):
    '''
    Test user get by using /api/session and TEST_USER_SIGNUP.
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    sessionid = data['content']['sessionID']
    r=client.delete("/api/session", {'sessionID': sessionid})
    assert r.status_code==200
    r = client.get("/api/user/"+sessionid)
    assert r.status_code == 200
    data = r.json()
    assert data['content']['degree'] == TEST_USER_SIGNUP['degree']
    assert data['content']['email'] == TEST_USER_SIGNUP['email']
    assert data['content']['major'] == TEST_USER_SIGNUP['major']
    assert data['content']['name'] == TEST_USER_SIGNUP['name']
    assert data['content']['phone'] == TEST_USER_SIGNUP['phone']
    assert data['content']['uid'] is not None



def test_put_user_success(client:Client,post_user):
    '''
    Test user put by changing TEST_USER_SIGNUP to TEST_USER_SIGNUP2
    compare the user information with TEST_USER_SIGNUP2
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    sessionid = data['content']['sessionID']
    TEST_USER_SIGNUP2['sessionID'] = data['content']['sessionID']
    r = client.put("/api/user",json = TEST_USER_SIGNUP2)
    assert r.status_code == 200


    r = client.post("/api/session", json=TEST_USER2)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP2['name']


    r = client.get("/api/user/"+data['content']['sessionID'])
    assert r.status_code == 200
    data = r.json()
    assert data['content']['degree'] == TEST_USER_SIGNUP2['degree']
    assert data['content']['email'] == TEST_USER_SIGNUP2['email']
    assert data['content']['major'] == TEST_USER_SIGNUP2['major']
    assert data['content']['name'] == TEST_USER_SIGNUP2['name']
    assert data['content']['phone'] == TEST_USER_SIGNUP2['phone']
    assert data['content']['uid'] is not None
    r=client.delete("/api/session", {'sessionID': sessionid})


def test_put_user_after_session_closed(client:Client,post_user):
    '''
    Test user put by changing TEST_USER_SIGNUP to TEST_USER_SIGNUP2
    compare the user information with TEST_USER_SIGNUP2
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']

    TEST_USER_SIGNUP2['sessionID'] = data['content']['sessionID']
    r = client.put("/api/user",json = TEST_USER_SIGNUP2)
    assert r.status_code == 200


    r = client.post("/api/session", json=TEST_USER2)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP2['name']


    r = client.get("/api/user/"+data['content']['sessionID'])
    assert r.status_code == 200
    data = r.json()
    assert data['content']['degree'] == TEST_USER_SIGNUP2['degree']
    assert data['content']['email'] == TEST_USER_SIGNUP2['email']
    assert data['content']['major'] == TEST_USER_SIGNUP2['major']
    assert data['content']['name'] == TEST_USER_SIGNUP2['name']
    assert data['content']['phone'] == TEST_USER_SIGNUP2['phone']
    assert data['content']['uid'] is not None