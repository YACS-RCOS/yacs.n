from .util import Client

#NOTE: Currently unable to test for non-public semesters access if
#User is admin

def test_success(upload, client: Client):
    #Make sure the upload works
    assert upload.status_code == 200
    params = {'semester' : 'SPRING 2020', 'search' : 'NUMERICAL COMPUTING'}
    r = client.get("/api/class", params = params)
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 13


def test_wrong_semester(upload, client: Client):
    assert upload.status_code == 200
    params = {'semester' : 'RANDOM'}
    r = client.get("/api/class", params = params)
    assert r.status_code == 401
    assert (r.text == "Semester isn't available")

def test_no_args(upload, client: Client):
    assert upload.status_code == 200
    r = client.get("/api/class")
    assert(r.text == "missing semester option")
