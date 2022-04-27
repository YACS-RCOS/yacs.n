import asyncio
from fastapi.testclient import TestClient
from models import AdminSettings
import pytest

@pytest.mark.tortoise
@pytest.mark.testclient
def test_default_semester_success(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    event_loop.run_until_complete(AdminSettings.all().delete())
    event_loop.run_until_complete(AdminSettings.create(semester="SUMMER 2020"))
    r = client.get("/api/defaultsemester")
    data = r.json()

    assert data == "SUMMER 2020"