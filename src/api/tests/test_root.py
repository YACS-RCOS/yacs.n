import pytest
import requests
from .util import Client
from .fixtures import *

def test_root(client: Client):
    r = client.get("/")
    assert(r.text == "YACS API is Up!")

def test_api(upload, client: Client):
    r = client.get("/api")
    assert(r.text == "wow")