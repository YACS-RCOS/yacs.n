import pytest
from fastapi import TestClient
@pytest.mark.testclient

def test_semester(upload, client: TestClient):
    """
    semester endpoint should get all of the semesters in the upload
    in the case of our test data, we should be getting get 2 semesters: "SUMMER 2020" and "SPRING 2020"
    """
    r = client.get("/api/semester")
    data = r.json()
    assert len(data) == 2
    assert data[0]["semester"] == "SUMMER 2020"
    assert data[1]["semester"] == "SPRING 2020"