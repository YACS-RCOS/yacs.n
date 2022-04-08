from fastapi.testclient import TestClient
import pytest

TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

@pytest.mark.testclient
def test_session_post_success(post_user, client: TestClient):
    '''
    Test session post with valid credentials
    '''
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200

    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == "TestName"
    client.delete("/api/session", json={'sessionID': data['content']['sessionID']})

@pytest.mark.testclient
def test_session_post_failure(client: TestClient):
    '''
    Test session post with invalid credentials
    '''
    r = client.post("/api/session", json={'email':'NotAUser', 'password':'000000'})
    assert r.status_code == 200

    data = r.json()
    assert data['content'] is None

@pytest.mark.testclient
def test_session_delete_success(post_user, client: TestClient):
    '''
    Test session delete with valid input
    '''
    sess = client.post("/api/session", json=TEST_USER).json()
    sessID = sess['content']['sessionID']
    r = client.delete('/api/session', json={'sessionID': sessID})
    assert r.status_code == 200
    assert r.json()['success'] == True

@pytest.mark.testclient
def test_session_delete_failure(client: TestClient):
    '''
    Test session delete with invalid session id
    '''
    r = client.delete('/api/session', json={'sessionID': 'not-a-session-id'})
    assert r.status_code == 200
    assert r.json()['success'] == False
