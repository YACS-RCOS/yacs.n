
from .util import Client

    #semester should get all of the semesters in the upload
    #in the case of our test data, we should be getting Summer and Spring semester of 2020
def test_semester(upload, client):
    r = client.get("/api/semester")
    print(r.text)
    data = r.json()
    assert len(data) == 2
    assert data[0]["semester"] == "SUMMER 2020"
    assert data[1]["semester"] == "SPRING 2020"