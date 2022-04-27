from fastapi.testclient import TestClient
import asyncio
from models import SemesterDateRange
import pytest

@pytest.mark.testclient
@pytest.mark.tortoise
def test_map_date_range(client: TestClient, event_loop:asyncio.AbstractEventLoop):
    r = client.post('/api/mapDateRangeToSemesterPart', data=[
        ('semesterTitle', 'SUMMER 2020'), ('isPubliclyVisible', 'true'), 
        ('date_start', '2020-05-26'), ('date_start', '2020-05-26'), 
        ('date_start', '2020-07-13'), ('date_end', '2020-08-21'), 
        ('date_end', '2020-07-10'), ('date_end', '2020-08-21'), 
        ('semester_part_name', '5/26 - 8/22'), ('semester_part_name', '5/26 - 7/10'), 
        ('semester_part_name', '7/13 - 8/21')])

    user = event_loop.run_until_complete(SemesterDateRange.get(date_start="2020-05-26", date_end = "2020-08-21"))
    assert user.date_start == "2020-05-26" and user.date_end == "2020-08-21" and user.semester_part_name == "5/26 - 8/22"

    user = event_loop.run_until_complete(SemesterDateRange.get(date_start="2020-05-26", date_end = "2020-07-10"))
    assert user.date_start == "2020-05-26" and user.date_end == "2020-07-10" and user.semester_part_name == "5/26 - 7/10"

    user = event_loop.run_until_complete(SemesterDateRange.get(date_start="2020-07-13", date_end = "2020-08-21"))
    assert user.date_start == "2020-07-13" and user.date_end == "2020-08-21" and user.semester_part_name == "7/13 - 8/21"

    assert r.status_code == 200

@pytest.mark.testclient
@pytest.mark.tortoise
def test_map_date_range_failure(client: TestClient, event_loop:asyncio.AbstractEventLoop):
    r = client.post('/api/mapDateRangeToSemesterPart', data=[
        ('semesterTitle', 'SUMMER 2020'), ('isPubliclyVisible', 'true'), 
        ('date_start', '2020-01-01'), ('date_start', '2020-01-01'), 
        ('date_start', '2020-01-01'), ('date_end', '2020-08-21'), 
        ('date_end', '2020-07-10'), ('date_end', '2020-08-21')])

    result = event_loop.run_until_complete(SemesterDateRange.filter(date_start="2020-01-01"))
    assert len(result) == 0 

    assert r.status_code == 500
