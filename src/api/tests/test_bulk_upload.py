import pytest
import requests
from .util import Client
from .fixtures import *

def test_bulk_upload(upload, client: Client):
    '''
    Test bulk upload. This will upload data and verify the data is received and stored.
    We will simply verify that the correct semesters are now available.
    '''
    assert upload.status_code == 200 # Verify Success status is returned

    # Get semesters
    expected_results = ['SUMMER 2020', 'SPRING 2020']
    r = client.get("/api/semester")
    assert r.status_code == 200
    semesters = [s['semester'] for s in r.json()]
    for s in expected_results:
        assert(s in semesters)