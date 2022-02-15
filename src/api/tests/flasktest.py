from .util import Client
TEST_USER = { 'email': 'og@gmail.com',
              'password': '200330chen' }
def test_user_post_success(post_user, client: Client):
    '''
    add a valid new user into the session
    '''
    r = client.post("/api/user", json=['abcd', 'g789@gmail.com', '', 'bbccchen1890', '', ''])
    assert r.status_code == 200
    data = r.json()
    assert data['content'] == "User added successfully."

