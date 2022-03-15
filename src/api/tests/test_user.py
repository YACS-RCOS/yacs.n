from .util import Client
TEST_USER = { 'email': 'test@email.com',
              'password': '123456' }

TEST_USER_SIGNUP = { 'email': 'test@email.com',
                     'name': 'TestName',
                     'phone': '',
                     'password': '123456',
                     'degree': 'Undergraduate',
                     'major': 'CSCI' }

# pytest -s tests/test_user.py
def test_user_post_success(post_user, client: Client):
    '''
    add a valid new user into the session
    '''
    r = client.post("/api/user", json= {"name": "test2", "email":"test12@gmail.com","phone": "", "password":"test123", "major":"", "degree":""} )
    data = r.json()
    assert r.status_code == 200
    assert data['content'] is not None
    assert data['content']['msg'] == "User added successfully."
    r = client.post('/api/session', json={"email":"test12@gmail.com", "password":"test123"})
    client.delete("/api/user", json={"sessionID":r.json()['content']['sessionID'], 'password':'test123'})

def test_user_post_failure(post_user, client: Client):
    '''
    add a invalid new user into the session
    '''
    r = client.post("/api/user", json= {"name": "test1", "email":"test1","phone": "", "password":"123", "major":"", "degree":""})
    data = r.json()
    assert data['content'] is None
    
def test_user_delete_success(post_user, client: Client):
    '''
    delete a valid user in the session
    '''
    r1 = client.post("/api/session", json=TEST_USER) # {'email':'test12@gmail.com', 'password': 'test123'})
    data = r1.json()
    sessionid = data['content']['sessionID']
    r2 = client.delete("/api/user", json= {"sessionID": sessionid, "password": "123456"})
    assert r2.status_code == 200
    r=client.post('/api/user', json=TEST_USER_SIGNUP)
    assert r.status_code == 200
    data = r.json()
    # assert data['content'] is not None
    # assert data['content']['msg'] == "User added successfully."

def test_user_delete_failure(post_user, client: Client):
    '''
    delete a not exist user in the session
    '''
    r1 = client.post("/api/session", json=TEST_USER) # {'email':'test12@gmail.com', 'password': 'test123'})
    data = r1.json()
    sessionid = data['content']['sessionID']
    r2 = client.delete("/api/user", json= {"sessionID": sessionid, "password": "12345"})
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2['errMsg'] == "Wrong password."