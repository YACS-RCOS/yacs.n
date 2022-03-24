from .util import Client

def test_default_semester_set(client: Client):
    r = client.post('/api/defaultsemesterset', json = {'default' :'SPRING 2020'})
    assert r.status_code == 200
    r = client.get("/api/defaultsemester")
    data = r.json()
    assert data == "SPRING 2020"

    r = client.post('/api/defaultsemesterset', json = {'default' :'SUMMER 2020'})
    assert r.status_code == 200
    r = client.get("/api/defaultsemester")
    data = r.json()
    assert data == "SUMMER 2020"  
