import pytest
from fastapi.testclient import TestClient

@pytest.mark.testclient
def test_default_semester_success(client: TestClient, upload):
    r = client.get("/api/defaultsemester")
    data = r.json()

    assert data == "SUMMER 2020"
