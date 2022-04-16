import pytest
import asyncio
from fastapi.testclient import TestClient
import os, inspect
from models import Course, CourseSession, CoursePrerequisite, CourseCorequisite
from datetime import date, time
import pytz

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
    course1 = event_loop.run_until_complete(Course.get(crn="15486").only("crn", "title", "semester"))
    assert course1.crn == "15486"
    assert course1.title == "STUDENT SUCCESS LABS"
    assert course1.semester == "SUMMER 2020"

    # For course 2 we will check all fields that should be populated
    course2 = event_loop.run_until_complete(
        Course.get(crn="95659").only("crn", "section", "semester", "min_credits", "max_credits",
                                     "description", "frequency", "full_title", "date_start", "date_end",
                                     "department", "level", "title", "raw_precoreqs", "school",
                                     "seats_open", "seats_filled", "seats_total"))

    assert course2.crn == "95659" and course2.section == "01"
    assert course2.semester == "SPRING 2020"
    assert course2.min_credits == 4 and course2.max_credits == 4
    assert course2.description == "In this class, students will write on topics from their major discipline and investigate the kinds of texts that professionals in their field produce. They will identify and explore research questions, use discipline-specific library databases, and write research reports. In addition, they will develop effective note-taking and research skills and learn strategies for effective prose style. This is a communication-intensive course."
    assert course2.frequency == "Fall term annually."
    assert course2.full_title == "Research Writing"
    assert course2.date_start == date(2020, 1, 13) and course2.date_end == date(2020, 5, 8)
    assert course2.department == "WRIT" and course2.level == 4410
    assert course2.title == "RESEARCH WRITING"
    assert course2.raw_precoreqs == None
    assert course2.school == "Humanities, Arts and Social Sciences"
    assert course2.seats_open == 0 and course2.seats_filled == 19 and course2.seats_total == 19

    # Need to check all tables, not just Course
    session = event_loop.run_until_complete(
        CourseSession.get(crn="95659", section="01", semester="SPRING 2020", day_of_week=1).only(
            "crn", "section", "semester", "time_start", "time_end",
            "day_of_week", "location", "session_type", "instructor"))
    assert session.crn == "95659" and session.section == "01"
    assert session.semester == "SPRING 2020"
    assert session.time_start == time(10, 0, tzinfo=pytz.timezone("UTC"))
    assert session.time_end == time(11, 50, tzinfo=pytz.timezone("UTC"))
    assert session.day_of_week == 1
    assert session.location == "VORHES NO"
    assert session.session_type == "LEC"
    assert session.instructor == "Lewis"

# BIOMEDICAL ENGINEERING LAB,LEC,4,W,9:00AM,11:00AM,Agarwal,,12,9,3,BMED,2020-05-26,2020-08-21,SUMMER 2020,15297,4010,01,BMED-4010,Biomedical Engineering Laboratory,"Theory and practice of biomedical measurements. An introduction to instrumentation and procedures for measurement of membrane transport, bioelectrical potentials, cell counting, biomechanical and biomaterial properties using invasive and noninvasive techniques. Transducers studied include strain gauge, differential transformer, spectrophometer, bipotential electrodes, microscope with camera, mechanical testing machine, piezoelectric transducer (or sensor). Also studied are instruments for determination of material properties.","Corequisite:  BMED 4200 or permission of instructor. Prerequisites: BMED 2100, BMED 2300, and BMED 2540",Fall and spring terms annually.,"['BMED-2100', 'BMED-2300', 'BMED-2540']",['BMED-4200'],Engineering
    # Course 2 does not have pre/corequisites, so we will use Biomedical Engineering Lab to verify those tables
    prereqs = event_loop.run_until_complete(
        CoursePrerequisite.filter(department="BMED", level=4010))
    assert prereqs[0].department == "BMED" and prereqs[0].level == 4010


@pytest.mark.testclient
@pytest.mark.tortoise
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
@pytest.mark.tortoise
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
