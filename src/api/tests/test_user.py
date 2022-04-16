import asyncio
from fastapi.testclient import TestClient
from models import UserAccount
import pytest

TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

TEST_USER_SIGNUP = { 'email': 'test@email.com',
                     'name': 'TestName',
                     'phone': '',
                     'password': '123456',
                     'degree': 'Undergraduate',
                     'major': 'CSCI' }

TEST_USER_SIGNUP_REVERT = { 'email': 'test@email.com',
                     'name': 'TestName',
                     'phone': '',
                     'newPassword': '123456',
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


@pytest.mark.testclient
@pytest.mark.tortoise
def test_user_post_success(post_user, client: TestClient, event_loop: asyncio.AbstractEventLoop):
    '''
    add a valid new user into the session
    '''
    r = client.post("/api/user", json= {"name": "test2", "email":"test12@gmail.com","phone": "", "password":"test123", "major":"", "degree":""} )
    data = r.json()
    assert r.status_code == 200
    assert data['content'] is not None
    assert data['content']['msg'] == "User added successfully."

    user = event_loop.run_until_complete(UserAccount.get(email="test12@gmail.com"))
    assert user is not None
    assert user.name == "test2"

@pytest.mark.testclient
@pytest.mark.tortoise
def test_user_post_failure(post_user, client: TestClient):
    '''
    add a invalid new user into the session
    '''
    r = client.post("/api/user", json= {"name": "test1", "email":"test1","phone": "", "password":"123", "major":"", "degree":""})
    data = r.json()
    assert data['content'] is None
    assert r.status_code == 200
    
@pytest.mark.testclient
@pytest.mark.tortoise
def test_user_delete_success(post_user, client: TestClient):
    '''
    delete a valid user in the session
    '''
    r1 = client.post("/api/session", json=TEST_USER)
    data = r1.json()
    sessionid = data['content']['sessionID']
    r2 = client.delete("/api/user", json= {"sessionID": sessionid, "password": "123456"})
    assert r2.status_code == 200
    r=client.post('/api/user', json=TEST_USER_SIGNUP)
    assert r.status_code == 200
    data = r.json()

@pytest.mark.testclient
@pytest.mark.tortoise
def test_user_delete_failure(post_user, client: TestClient):
    '''
    delete a not exist user in the session
    '''
    r1 = client.post("/api/session", json=TEST_USER)
    data = r1.json()
    sessionid = data['content']['sessionID']
    r2 = client.delete("/api/user", json= {"sessionID": sessionid, "password": "12345"})
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2['errMsg'] == "Wrong password."

@pytest.mark.testclient
@pytest.mark.tortoise
def test_user_delete_failure2(post_user, client: TestClient):
    '''
    delete the session, then try to delete user
    '''
    sess = client.post("/api/session", json=TEST_USER).json()
    sessID = sess['content']['sessionID']
    r = client.delete('/api/session', json={'sessionID': sessID})
    assert r.status_code == 200
    r1 = client.delete("/api/user", json= {"sessionID": sessID, "password": "12345"})
    assert r1.status_code == 403

@pytest.mark.testclient
@pytest.mark.tortoise
def test_get_user_success(client: TestClient, post_user):
    '''
    Test user get by using /api/session and TEST_USER_SIGNUP.
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    sessionid = data['content']['sessionID']
    r = client.get("/api/user/"+sessionid)
    assert r.status_code == 200
    data = r.json()
    assert data['content']['degree'] == TEST_USER_SIGNUP['degree']
    assert data['content']['email'] == TEST_USER_SIGNUP['email']
    assert data['content']['major'] == TEST_USER_SIGNUP['major']
    assert data['content']['name'] == TEST_USER_SIGNUP['name']
    assert data['content']['phone'] == TEST_USER_SIGNUP['phone']
    assert data['content']['uid'] is not None
    client.delete("/api/session", json={'sessionID': sessionid})

@pytest.mark.testclient
@pytest.mark.tortoise
def test_get_user_failed(client: TestClient,post_user):
    '''
    Test user get with invalid sessionID
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200

    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    sessionid = data['content']['sessionID']

    r = client.get("/api/user/"+"00000000")
    assert r.status_code == 200
    data = r.json()
    assert data['errMsg'] == "Unable to find the session."
    client.delete("/api/session", json={'sessionID': sessionid})

@pytest.mark.testclient
@pytest.mark.tortoise
def test_get_user_after_session_closed(client: TestClient,post_user):
    '''
    Test user get by using /api/session and TEST_USER_SIGNUP after session is closed.
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    sessionid = data['content']['sessionID']
    r=client.delete("/api/session", json={'sessionID': sessionid})
    assert r.status_code==200
    r = client.get("/api/user/"+sessionid)
    assert r.status_code == 403


@pytest.mark.testclient
@pytest.mark.tortoise
def test_put_user_success(client:TestClient,post_user):
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

    r=client.delete("/api/session", json={'sessionID': sessionid})
    r = client.post("/api/session", json=TEST_USER2)
    assert r.status_code == 200
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP2['name']
    sessionid = data['content']['sessionID']

    r = client.get("/api/user/"+data['content']['sessionID'])
    assert r.status_code == 200
    data = r.json()
    assert data['content']['degree'] == TEST_USER_SIGNUP2['degree']
    assert data['content']['email'] == TEST_USER_SIGNUP2['email']
    assert data['content']['major'] == TEST_USER_SIGNUP2['major']
    assert data['content']['name'] == TEST_USER_SIGNUP2['name']
    assert data['content']['phone'] == TEST_USER_SIGNUP2['phone']
    assert data['content']['uid'] is not None
    TEST_USER_SIGNUP_REVERT['sessionID'] = sessionid
    r = client.put("/api/user",json = TEST_USER_SIGNUP_REVERT)

    r=client.delete("/api/session", json={'sessionID': sessionid})


@pytest.mark.testclient
@pytest.mark.tortoise
def test_put_user_after_session_closed(client:TestClient,post_user):
    '''
    Test user put by changing TEST_USER_SIGNUP to TEST_USER_SIGNUP2
    after session is closed
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    data = r.json()

    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    sessionid = data['content']['sessionID']

    TEST_USER_SIGNUP2['sessionID'] = data['content']['sessionID']
    r=client.delete("/api/session", json={'sessionID': sessionid})
    r = client.put("/api/user",json = TEST_USER_SIGNUP2)
    assert r.status_code == 403