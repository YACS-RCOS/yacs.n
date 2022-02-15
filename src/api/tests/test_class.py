from .util import Client

def test_success(upload, client: Client):
    #Make sure the upload works
    assert upload.status_code == 200
    r = client.get("/api/class?semester=SPRING%202020&search=NUMERICAL%20COMPUTING")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 13


def test_wrong_semester(upload, client: Client):
    assert upload.status_code == 200
    r = client.get("/api/class?semester=RANDOM")
    assert r.status_code == 401
    assert (r.text == "Semester isn't available")

def test_no_args(upload, client: Client):
    assert upload.status_code == 200
    r = client.get("/api/class")
    assert(r.text == "missing semester option")
