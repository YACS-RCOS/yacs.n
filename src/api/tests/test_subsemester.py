from .util import Client

    #when given an input such as Spring 2020 subsemester it should only return data for that subsemester
def test_subsemeseter_spring2020(client, upload):
    r = client.get("/api/subsemester",
                params={"semester":"SPRING 2020"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["parent_semester_name"] == "SPRING 2020"

    #when no subsemester is taken as input the API should return all of the subsemesters
def test_subsemester_nosemester(client, upload):
    r = client.get("/api/subsemester")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 4

    #invalid semester input should return no semesters
def test_subsemester_invalid_semester(client):
    r = client.get("/api/subsemester", params={"semester":"moon 2050"})
    print(r.text)
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0
    