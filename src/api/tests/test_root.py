import pytest
import requests
from util import Client

@pytest.fixture
def client():
    return Client()

def test_root(client: Client):
    r = client.get("/")
    assert(r.text == "YACS API is Up!")

def test_api(client: Client):
    r = client.get("/api")
    assert(r.text == "wow")