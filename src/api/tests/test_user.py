from .util import Client
TEST_USER = { 'email': 'og@gmail.com',
              'password': '200330chen' }

# pytest -s tests/test_user.py
def test_user_post_success(post_user, client: Client):
    '''
    add a valid new user into the session
    '''
    r = client.post("/api/user", json= {"name": "test2", "email":"test2@gmai.com","phone": "", "password":"test123", "major":"", "degree":""} )
    print(r.json())
    data = r.json()
    assert data['content'] is not None
    assert data['content']['msg'] == "User added successfully."

def test_user_post_failure(post_user, client: Client):
    '''
    add a invalid new user into the session
    '''
    r = client.post("/api/user", json= {"name": "test1", "email":"test1","phone": "", "password":"123", "major":"", "degree":""})
    data = r.json()
    print(r.json())
    assert data['content'] is None
    
