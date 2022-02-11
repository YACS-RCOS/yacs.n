from .util import Client
from .fixtures import *

def test_bulk_upload_success(upload, client: Client):
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
        assert s in semesters

def test_bulk_upload_no_file(client: Client):
    '''
    Tests bulk course upload for when no file is provided
    '''
    multipart_form_data = (
        ('file', ('test_data.csv', None)),
        ('isPubliclyVisible', (None, "on")),
    )
    r = client.post("/api/bulkCourseUpload",
                    files=multipart_form_data)
    assert r.status_code == 400

def test_bulk_upload_wrong_file_extension(client: Client):
    '''
    Tests bulk course upload for when a non-csv file is provided
    '''
    multipart_form_data = (
        ('file', ('test_bulk_upload.py', open('tests/test_bulk_upload.py', 'rb'))),
        ('isPubliclyVisible', (None, "on")),
    )
    r = client.post("/api/bulkCourseUpload",
                    files=multipart_form_data)
    assert r.status_code == 400
