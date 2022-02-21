from .util import Client



TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

TEST_COURSE = {'name': 'ARCH-4770',
               'cid': '-1',
               'semester': 'SUMMER2020'}


# TEST_USER_COURSE = {'name': 'ADMN-1824',
#                     'semester': 'SUMMER 2020',
#                     'cid': '-1'
# }


def test_user_course_get_success(post_user, client: Client):
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    course = client.post("/api/user/course", json=TEST_COURSE)
    assert course.status_code == 200
    d = client.get("/api/user/course", json=TEST_COURSE)
    data = d.json()[2]
    print(d.json())
    assert data['course_name'] == TEST_COURSE['name']
    assert data['crn'] == TEST_COURSE['cid']
    assert data['semester'] == TEST_COURSE['semester']



# [{'course_name': 'ADMN-1824', 'crn': '-1', 'semester': 'SUMMER 2020'}, {'course_name': 'ADMN-1824', 'crn': '15486', 'semester': 'SUMMER 2020'}, {'course_name': 'ARCH-4770', 'crn': '-1', 'semester': 'SUMMER2020'}, {'course_name': 'ARCH-4770', 'crn': '-1', 'semester': 'SUMMER 2020'}, {'course_name': 'ARCH-4770', 'crn': '15413', 'semester': 'SUMMER 2020'}, {'course_name': 'ARCH-4770', 'crn': '15769', 'semester': 'SUMMER 2020'}, {'course_name': 'ARCH-4770', 'crn': '15815', 'semester': 'SUMMER 2020'}, {'course_name': 'ARCH-4780', 'crn': '-1', 'semester': 'SUMMER 2020'}, {'course_name': 'ARCH-4780', 'crn': '15771', 'semester': 'SUMMER 2020'}, {'course_name': 'ARCH-4780', 'crn': '15772', 'semester': 'SUMMER 2020'}, {'course_name': 'ARCH-4780', 'crn': '15816', 'semester': 'SUMMER 2020'}, {'course_name': 'ARTS-1380', 'crn': '-1', 'semester': 'SUMMER 2020'}, {'course_name': 'ARTS-1380', 'crn': '15710', 'semester': 'SUMMER 2020'}]