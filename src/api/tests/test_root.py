from fastapi.testclient import TestClient
import pytest

def test_root(client: TestClient):
    r = client.get("/")
    assert(r.text == "YACS API is Up!")

def test_api(client: TestClient):
    r = client.get("/api")
    assert(r.text == "wow")
