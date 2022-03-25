import pytest
from fastapi import TestClient
from typing import Optional
from fastapi import Depends, FastAPI

@pytest.mark.testclient
def test_subsemeseter_spring2020(client: TestClient, upload):
    """
    when subsemester endpoint is given an input such as Spring 2020 
    it should only return data for that subsemester i.e. data where the parent semester name 
    is "SPRING 2020".
    """
    r = client.get("/api/subsemester",
                params={"semester":"SPRING 2020"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["parent_semester_name"] == "SPRING 2020"

def test_subsemester_nosemester(client, upload):
    """   
    when no subsemester is taken as input the subsemester endpoint should return all of the subsemesters
    contained in the upload data.
    Specifically there should be 4 total returned semesters
    """
    r = client.get("/api/subsemester")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 4

def test_subsemester_invalid_semester(client):
    """
    invalid input to subsemester to subsemester endpoint such as "moon 2050" 
    should result in an empty list of semester data being returned.
    The status should still be success, and size of the data should be 0.
    """
    r = client.get("/api/subsemester", params={"semester":"moon 2050"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0
    