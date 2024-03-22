import pytest
from fastapi.testclient import TestClient

@pytest.mark.testclient
def test_semester_info_success(client: TestClient, _upload):
    r = client.get("/api/semesterInfo")
    data = r.json()
    assert len(data) == 2

    semesters = [d["semester"] for d in data]
    assert "SUMMER 2020" in semesters
    assert "SPRING 2020" in semesters

    assert data[0]["public"]
    assert data[1]["public"]
