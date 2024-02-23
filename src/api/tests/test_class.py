from fastapi.testclient import TestClient 
import pytest

#NOTE: Currently unable to test for non-public semesters access if
#User is admin

@pytest.mark.testclient
def test_success(upload, client: TestClient):
    #Make sure the upload works
    assert upload.status_code == 200
    params = {'semester' : 'SPRING 2020', 'search' : 'NUMERICAL COMPUTING'}
    r = client.get("/api/class", params = params)
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 13

@pytest.mark.testclient
def test_wrong_semester(upload, client: TestClient):
    assert upload.status_code == 200
    params = {'semester' : 'RANDOM'}
    r = client.get("/api/class", params = params)
    assert r.status_code == 401
    assert r.text == "Semester isn't available"

@pytest.mark.testclient
def test_no_args(upload, client: TestClient):
    assert upload.status_code == 200
    r = client.get("/api/class")
    assert r.text == "missing semester option"
