from fastapi.testclient import TestClient 
import pytest

def test_department_success(upload, client: TestClient):
    assert upload.status_code == 200

    #Some sample of the departments that we make sure exist
    expected = ['ADMN', 'LANG', 'MATH', 'CSCI', 'ECON', 'MATP']
    r = client.get("/api/department")
    assert r.status_code == 200
    data = r.json()
    #Make sure the right number of departments exist
    assert len(data) == 43
    departments = [d['department'] for d in data]
    for d in expected:
        assert d in departments
