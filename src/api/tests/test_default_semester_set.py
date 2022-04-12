
import asyncio
from fastapi.testclient import TestClient
from models import UserAccount
import pytest
@pytest.mark.tortoise
@pytest.mark.testclient
def test_default_semester_set(client: TestClient,event_loop: asyncio.AbstractEventLoop):
    r = client.post('/api/defaultsemesterset', json = {'default' :'SUMMER 2020'})
    assert r.status_code == 200
    # r = client.get("/api/defaultsemester")
    # data = r.json()
    data = event_loop.run_until_complete(UserAccount.get(email="test12@gmail.com"))
    assert data == "SUMMER 2020"  
    
    r = client.post('/api/defaultsemesterset', json = {'default' :'SPRING 2020'})
    assert r.status_code == 200
    r = client.get("/api/defaultsemester")
    data = r.json()
    assert data == "SPRING 2020"
