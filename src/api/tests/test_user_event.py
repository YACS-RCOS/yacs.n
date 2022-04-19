import asyncio
from fastapi.testclient import TestClient
from models import UserEvent
import pytest

TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

@pytest.mark.testclient
@pytest.mark.tortoise
def test_add_user_event_success(post_user, client: TestClient, event_loop: asyncio.AbstractEventLoop):
    '''
    add a valid new user into the session
    ['uid', 'eventID', 'data', 'createdAt']
    '''
    r1 = client.post("/api/session", json=TEST_USER)
    data = r1.json()
    sessionid = data['content']['sessionID']
    r = client.post("/api/event", json= {"uid": "0001", "eventID":"0001","data":"aa","createdAt": "0000","email": "test@email.com", "password": "123456"} )
    data = r.json()
    print(data)
    assert r.status_code == 200
    # assert data['content'] is not None

    userEvent = event_loop.run_until_complete(UserEvent.get(user_id="0001",event_id = "0001"))
    assert userEvent is not None
    assert userEvent.data == "a"
    assert userEvent.data == "0000"
    
