import asyncio
from fastapi.testclient import TestClient
from models import UserEvent
import pytest


@pytest.mark.testclient
@pytest.mark.tortoise
def test_user_post_success(post_user, client: TestClient, event_loop: asyncio.AbstractEventLoop):
    '''
    add a valid new user into the session
    ['uid', 'eventID', 'data', 'createdAt']
    '''
    r = client.post("/api/event", json= {"uid": "0001", "eventID":"0001","data":"aa","createdAt": "0000"} )
    data = r.json()
    print(data)
    assert r.status_code == 200
    assert data['content'] is not None
    assert data['content']['msg'] == "User added successfully."

    userEvent = event_loop.run_until_complete(UserEvent.get(uid="0001",eventID ="0001" ))
    assert userEvent is not None
    assert userEvent.data == "a"
    assert userEvent.data == "0000"
    
