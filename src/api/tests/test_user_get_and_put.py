from urllib import response
import pytest
import requests
from .util import Client
# from .fixtures import *


TEST_USER = { 'email': "test@email.com",
              'password': "123456" }



TEST_USER_SIGNUP = { 'email': 'test@email.com',
                     'name': 'TestName',
                     'phone': '',
                     'password': '123456',
                     'degree': 'Undergraduate',
                     'major': 'CSCI' }


TEST_USER2 = { 'email': "test2@email.com",
              'password': "1234567" }


TEST_USER_SIGNUP2 = { 'email': 'test2@email.com',
                     'name': 'TestName2',
                     'phone': '',
                     'newPassword': '1234567',
                     'degree': 'Graduate',
                     'major': 'ECON' }

def test_get_user_success(client: Client):

    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    headersa = r.headers
    #print (headersa['set-cookie'])
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


def test_put_user_success(client:Client):
    r = client.post("/api/session", json=TEST_USER)
    assert r.status_code == 200
    headersa = r.headers
    #print (headersa['set-cookie'])
    print ("first time:",r.headers)
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP['name']

    TEST_USER_SIGNUP2['sessionID'] = data['content']['sessionID']
    print ("test2:",TEST_USER_SIGNUP2)
    r = client.put("/api/user",json = TEST_USER_SIGNUP2,headers = {'Cookie': headersa['set-cookie']})
    assert r.status_code == 200
    print (r.content)


    r = client.post("/api/session", json=TEST_USER2)
    assert r.status_code == 200
    headersa = r.headers
    print ("second time:",r.headers, r.json())
    # print (headersa['set-cookie'])
    data = r.json()
    assert data['content'] is not None
    assert data['content']['sessionID'] is not None
    assert data['content']['userName'] == TEST_USER_SIGNUP2['name']


    r = client.get("/api/user/"+data['content']['sessionID'],headers = {'Cookie': headersa['set-cookie']})
    assert r.status_code == 200
    data = r.json()
    assert data['content']['degree'] == TEST_USER_SIGNUP2['degree']
    assert data['content']['email'] == TEST_USER_SIGNUP2['email']
    assert data['content']['major'] == TEST_USER_SIGNUP2['major']
    assert data['content']['name'] == TEST_USER_SIGNUP2['name']
    assert data['content']['phone'] == TEST_USER_SIGNUP2['phone']
    assert data['content']['uid'] is not None