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

# pytest -s tests/test_user.py
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
# @pytest.mark.tortoise
def test_user_delete_success(post_user, client: TestClient):
    '''
    delete a valid user in the session
    '''
    r1 = client.post("/api/session", json=TEST_USER) # {'email':'test12@gmail.com', 'password': 'test123'})
    data = r1.json()
    sessionid = data['content']['sessionID']
    r2 = client.delete("/api/user", json= {"sessionID": sessionid, "password": "123456"})
    assert r2.status_code == 200
    r=client.post('/api/user', json=TEST_USER_SIGNUP)
    assert r.status_code == 200
    data = r.json()

@pytest.mark.testclient
# @pytest.mark.tortoise
def test_user_delete_failure(post_user, client: TestClient):
    '''
    delete a not exist user in the session
    '''
    r1 = client.post("/api/session", json=TEST_USER) # {'email':'test12@gmail.com', 'password': 'test123'})
    data = r1.json()
    sessionid = data['content']['sessionID']
    r2 = client.delete("/api/user", json= {"sessionID": sessionid, "password": "12345"})
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2['errMsg'] == "Wrong password."

@pytest.mark.testclient
# @pytest.mark.tortoise
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