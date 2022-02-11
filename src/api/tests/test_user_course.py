import pytest
import requests
from .util import Client
from .fixtures import *

def test_user_course(client: Client):
    r = client.get("/api/user/course")
    assert(r.text == "YACS API is Up!")
