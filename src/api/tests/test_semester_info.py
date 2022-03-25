import pytest
from fastapi.testclient import TestClient

@pytest.mark.testclient
def test_semester_info_success(client: TestClient, upload):
    r = client.get("/api/semesterInfo")
    data = r.json()
    assert len(data) == 2
    assert data[0]["semester"] == "SUMMER 2020"
    assert data[1]["semester"] == "SPRING 2020"

    assert data[0]["public"] == True
    assert data[1]["public"] == True