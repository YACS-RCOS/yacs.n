import asyncio
from fastapi.testclient import TestClient
from models import UserAccount
import pytest
@pytest.mark.tortoise
@pytest.mark.testclient
def test_default_semester_success(client: TestClient, upload,event_loop: asyncio.AbstractEventLoop):
    r = client.get("/api/defaultsemester")
    data = r.json()

    assert data == "SUMMER 2020"