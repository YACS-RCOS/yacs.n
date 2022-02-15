from .util import Client

def test_success(upload, client: Client):
    #Make sure the upload works
    assert upload.status_code == 200

    #The below code caused errors for some reason
    #Check to make sure that the Fall 2020 semester is correctly received
    #params = {'semester':'FALL%202020', 'search':'EFF%20COMM%20FOR%20CLASS%20PEDAGOGY'}
    #r = client.get("/api/class", params=params)
    r = client.get("/api/class?semester=FALL%202020&search=EFF%20COMM%20FOR%20CLASS%20PEDAGOGY")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2


def test_wrong_semester(upload, client: Client):
    assert upload.status_code == 200
    r = client.get("/api/class?semester=RANDOM")
    assert r.status_code == 401
    assert (r.text == "Semester isn't available")

def test_no_args(upload, client: Client):
    assert upload.status_code == 200
    r = client.get("/api/class")
    assert(r.text == "missing semester option")
