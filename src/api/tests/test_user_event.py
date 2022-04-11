import asyncio
from fastapi.testclient import TestClient
from models import UserAccount
import pytest


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

