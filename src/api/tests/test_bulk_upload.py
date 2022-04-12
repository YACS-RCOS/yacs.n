import pytest
import asyncio
from fastapi.testclient import TestClient
import os, inspect
from models import Course

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
appdir = os.environ.get("TEST_APP_DIR", os.path.dirname(current_dir))

# {'name': 'ADMN-1824',
#                     'semester': 'SUMMER 2020',
#                     'cid': '-1'}

@pytest.mark.testclient
@pytest.mark.tortoise
def test_bulk_upload_success(upload, client: TestClient, event_loop: asyncio.AbstractEventLoop):
    '''
    Test bulk upload. This will upload data and verify the data is received and stored.
    We will simply verify that the correct semesters are now available.
    '''
    assert upload.status_code == 200 # Verify Success status is returned

    # Check for a course from each semester in test data
    course1 = event_loop.run_until_complete(Course.get(crn="15486"))
    assert course1.full_title == "STUDENT SUCCESS LABS"
    assert course1.semester == "SUMMER 2020"

    course2 = event_loop.run_until_complete(Course.get(crn="95659"))
    assert course2.full_title == "RESEARCH WRITING"
    assert course2.semester == "SPRING 2020"

    # Get semesters
    # expected_results = ['SUMMER 2020', 'SPRING 2020']
    # r = client.get("/api/semester")
    # assert r.status_code == 200
    # semesters = [s['semester'] for s in r.json()]
    # for s in expected_results:
    #     assert s in semesters


@pytest.mark.testclient
def test_bulk_upload_no_file(client: TestClient):
    '''
    Tests bulk course upload for when no file is provided
    '''
    multipart_form_data = {
        'file': ('test_data.csv'),
        'isPubliclyVisible': (None, "on"),
    }
    r = client.post("/api/bulkCourseUpload",
                    files=multipart_form_data)
    assert r.status_code == 400

@pytest.mark.testclient
def test_bulk_upload_wrong_file_extension(client: TestClient):
    '''
    Tests bulk course upload for when a non-csv file is provided
    '''
    multipart_form_data = {
        'file': ('test_bulk_upload.py', open(appdir + '/tests/test_bulk_upload.py', 'rb')),
        'isPubliclyVisible': (None, "on"),
    }
    r = client.post("/api/bulkCourseUpload",
                    files=multipart_form_data)
    assert r.status_code == 400
