from urllib import response
import pytest
import requests
from .util import Client
from .fixtures import *


TEST_USER = { 'email': TEST_USER_SIGNUP['email'],
              'password': TEST_USER_SIGNUP['password'] }


'''
TEST_USER_SIGNUP = { 'email': 'test@email.com',
                     'name': 'TestName',
                     'phone': '',
                     'password': '123456',
                     'degree': 'Undergraduate',
                     'major': 'CSCI' }
'''

def test_get_user_success(client: Client):

    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    headersa = r.headers
    print (headersa['set-cookie'])
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    '''
    {degree: "Undergraduate", email: "test@email.com", major: "CSCI", name: "TestName", phone: "", uid: 1}
    '''
    r = client.get("/api/user/"+data['content']['sessionID'],headers = {'Cookie': headersa['set-cookie']})
    assert r.status_code == 200
    data = r.json()
    assert data['content']['degree'] == TEST_USER_SIGNUP['degree']
    assert data['content']['email'] == TEST_USER_SIGNUP['email']
    assert data['content']['major'] == TEST_USER_SIGNUP['major']
    assert data['content']['name'] == TEST_USER_SIGNUP['name']
    assert data['content']['phone'] == TEST_USER_SIGNUP['phone']
    assert data['content']['uid'] is not None
    #assert(r.text == "YACS API is Up!")

def test_get_user_no_cookie(client: Client):

    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    headersa = r.headers
    print (headersa['set-cookie'])
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    '''
    {degree: "Undergraduate", email: "test@email.com", major: "CSCI", name: "TestName", phone: "", uid: 1}
    '''
    r = client.get("/api/user/"+data['content']['sessionID'])
    assert r.status_code == 403
    # data = r.json()
    # assert data['content']['degree'] == TEST_USER_SIGNUP['degree']
    # assert data['content']['email'] == TEST_USER_SIGNUP['email']
    # assert data['content']['major'] == TEST_USER_SIGNUP['major']
    # assert data['content']['name'] == TEST_USER_SIGNUP['name']
    # assert data['content']['phone'] == TEST_USER_SIGNUP['phone']
    # assert data['content']['uid'] is not None
# def test_api(upload, client: Client):
#     r = client.get("/api")
#     assert(r.text == "wow")

def test_get_user_success(client: Client):

    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    headersa = r.headers
    print (headersa['set-cookie'])
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']
    '''
    {degree: "Undergraduate", email: "test@email.com", major: "CSCI", name: "TestName", phone: "", uid: 1}
    '''
    r = client.get("/api/user/"+"00000000",headers = {'Cookie': headersa['set-cookie']})
    assert r.status_code == 200
    data = r.json()
    assert data['errMsg'] == "Unable to find the session."
    # assert data['content']['degree'] == TEST_USER_SIGNUP['degree']
    # assert data['content']['email'] == TEST_USER_SIGNUP['email']
    # assert data['content']['major'] == TEST_USER_SIGNUP['major']
    # assert data['content']['name'] == TEST_USER_SIGNUP['name']
    # assert data['content']['phone'] == TEST_USER_SIGNUP['phone']
    # assert data['content']['uid'] is not None
    #assert(r.text == "YACS API is Up!")