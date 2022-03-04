from .util import Client

def test_default_semester_success(client: Client, upload):
    r = client.get("/api/defaultsemester")
    data = r.json()

    assert data == "SUMMER 2020"