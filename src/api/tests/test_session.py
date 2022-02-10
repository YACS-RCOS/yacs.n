from .util import Client
from .fixtures import *

TEST_USER = { 'email': TEST_USER_SIGNUP['email'],
              'password': TEST_USER_SIGNUP['password'] }

def test_session_post_success(post_user, client: Client):
    '''
    Test session post with valid credentials
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200

    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']

def test_session_post_failure(client: Client):
    '''
    Test session post with invalid credentials
    '''
    r = client.post("/api/session", json={'name':'NotAUser', 'password':'000000'})
    assert r.status_code == 200

    data = r.json()
    assert data['content'] is None

def test_session_delete_success(post_user, client: Client):
    '''
    Test session delete with valid input
    '''
    sess = client.post("/api/session", json=TEST_USER).json()
    sessID = sess['content']['sessionID']
    r = client.delete('/api/session', json={'sessionID': sessID})
    assert r.status_code == 200
    assert r.json()['success'] == True

def test_session_delete_failure(client: Client):
    '''
    Test session delete with invalid session id
    '''
    r = client.delete('/api/session', json={'sessionID': 'not-a-session-id'})
    assert r.status_code == 200
    assert r.json()['success'] == False
