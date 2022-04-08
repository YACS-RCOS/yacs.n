from fastapi.testclient import TestClient
import pytest

@pytest.mark.testclient
def test_map_date_range(client: TestClient):
    r = client.post('/api/mapDateRangeToSemesterPart', data=[
        ('semesterTitle', 'SUMMER 2020'), ('isPubliclyVisible', 'true'), 
        ('date_start', '2020-05-26'), ('date_start', '2020-05-26'), 
        ('date_start', '2020-07-13'), ('date_end', '2020-08-21'), 
        ('date_end', '2020-07-10'), ('date_end', '2020-08-21'), 
        ('semester_part_name', '5/26 - 8/22'), ('semester_part_name', '5/26 - 7/10'), 
        ('semester_part_name', '7/13 - 8/21')])

    assert r.status_code == 200

@pytest.mark.testclient
def test_map_date_range_failure(client: TestClient):
    r = client.post('/api/mapDateRangeToSemesterPart', data=[
        ('semesterTitle', 'SUMMER 2020'), ('isPubliclyVisible', 'true'), 
        ('date_start', '2020-05-26'), ('date_start', '2020-05-26'), 
        ('date_start', '2020-07-13'), ('date_end', '2020-08-21'), 
        ('date_end', '2020-07-10'), ('date_end', '2020-08-21')])

    assert r.status_code == 500
