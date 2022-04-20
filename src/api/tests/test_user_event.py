import asyncio
from fastapi.testclient import TestClient
from models import UserEvent
import pytest
import uuid
import time
import calendar

TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

@pytest.mark.testclient
@pytest.mark.tortoise
def test_add_user_event_success(post_user, client: TestClient, event_loop: asyncio.AbstractEventLoop):
    '''
    add a new user event
    '''
    sess=client.post("/api/session", json=TEST_USER)
    uid = uuid.uuid4()
    r = client.post("/api/event", json= {"uid": str(uid), "eventID":"1","data":"aa","createdAt": calendar.timegm(time.gmtime())} )
    data = r.json()
    assert r.status_code == 200
    userEvent = event_loop.run_until_complete(UserEvent.get(event_id = 1, user_id=str(uid)))
    assert userEvent is not None
    assert userEvent.content == "aa"
    client.delete("/api/session", json={"sessionID": sess.json()['content']['sessionID']})
    

@pytest.mark.testclient
@pytest.mark.tortoise
def test_add_user_event_failure(post_user, client: TestClient, event_loop: asyncio.AbstractEventLoop):
    '''
    add a new user event without log in
    '''
    uid = uuid.uuid4()
    r = client.post("/api/event", json= {"uid": str(uid), "eventID":"1","data":"aa","createdAt": calendar.timegm(time.gmtime())} )
    assert r.status_code == 403


@pytest.mark.testclient
@pytest.mark.tortoise
def test_update_user_event_success(post_user, client: TestClient, event_loop: asyncio.AbstractEventLoop):
    '''
    add a new user event
    '''
    sess=client.post("/api/session", json=TEST_USER)
    uid = uuid.uuid4()
    r = client.post("/api/event", json= {"uid": str(uid), "eventID":"2","data":"original","createdAt": calendar.timegm(time.gmtime())})
    client.delete("/api/session", json={"sessionID": sess.json()['content']['sessionID']})
    assert r.status_code == 200
    userEvent = event_loop.run_until_complete(UserEvent.get(event_id = 2, user_id=str(uid)))
    assert userEvent is not None
    assert userEvent.content == "original"
    # don't know why it need login again
    sess=client.post("/api/session", json=TEST_USER)
    r = client.put("/api/event", json= {"uid": str(uid), "eventID":"2","data":"changed"})
    client.delete("/api/session", json={"sessionID": sess.json()['content']['sessionID']})
    assert r.status_code == 200
    userEvent = event_loop.run_until_complete(UserEvent.get(event_id = 2, user_id=str(uid)))
    assert userEvent is not None
    assert userEvent.content == "changed"


@pytest.mark.testclient
@pytest.mark.tortoise
def test_update_user_event_failure(post_user, client: TestClient, event_loop: asyncio.AbstractEventLoop):
    '''
    update a new user event without log in
    '''
    uid = uuid.uuid4()
    r = client.put("/api/event", json= {"uid": str(uid), "eventID":"1","data":"aa" })
    assert r.status_code == 403