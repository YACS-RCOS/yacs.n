from .util import Client



TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

TEST_COURSE = {'name': 'ARCH-4770',
               'cid': '-1',
               'semester': 'SUMMER2020'}

TEST_COURSE_2 = {'name': 'ARCH-4770',
               'cid': None,
               'semester': 'SUMMER2020'}


def test_user_course_delete_success(post_user, client: Client):
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    course = client.post("/api/user/course", json=TEST_COURSE)
    assert course.status_code == 200
    d = client.get("/api/user/course", json=TEST_COURSE)
    print ("before delete",len(d.json()))
    data = d.json()[1]
    print(d.json())
    assert data['course_name'] == TEST_COURSE['name']
    assert data['crn'] == TEST_COURSE['cid']
    assert data['semester'] == TEST_COURSE['semester']
    x = client.delete("/api/user/course", json = TEST_COURSE)
    assert x.status_code == 200
    d = client.get("/api/user/course", json=TEST_COURSE)
    assert len(d.json()) ==1
    print("after delete",len(d.json()))
    client.delete("/api/session", json = {"sessionID": r.json()["content"]["sessionID"]})

def test_user_course_delete_failure(client: Client):
    r = client.post("/api/user/course", json=TEST_USER)
    assert r.status_code == 403
