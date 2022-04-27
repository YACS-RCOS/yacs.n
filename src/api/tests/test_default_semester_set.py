
import asyncio
from fastapi.testclient import TestClient
# from api.db.semester_info import semester_info
from models import AdminSettings
import pytest
@pytest.mark.tortoise
@pytest.mark.testclient
def test_default_semester_set(client: TestClient,event_loop: asyncio.AbstractEventLoop):
    r = client.post('/api/defaultsemesterset', json = {'default' :'SUMMER 2020'})
    assert r.status_code == 200
    d = event_loop.run_until_complete(AdminSettings.get(semester = 'SUMMER 2020'))
    assert d is not None
    assert d.semester == "SUMMER 2020"
    r = client.post('/api/defaultsemesterset', json = {'default' :'SPRING 2020'})
    assert r.status_code == 200
    d = event_loop.run_until_complete(AdminSettings.get(semester = 'SPRING 2020'))
    assert d is not None
    assert d.semester == "SPRING 2020"
