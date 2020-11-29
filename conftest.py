import os
import pytest

from src.api.db.connection import db
from src.api.db.classinfo import ClassInfo
from src.api.db.courses import Courses
from src.api.db.admin import Admin
from src.api.db.semester_info import semester_info as SemesterInfo
from src.api.db.semester_date_mapping import semester_date_mapping as SemesterDateMapping
# from src.api.db.student_course_selection import student_course_selection
# from src.api.db.user import User
from rpi_data.modules.add_school_column import SchoolDepartmentMapping, SCHOOL_DEPARTMENT_MAPPING_YAML_FILENAME
from rpi_data.modules.fetch_catalog_course_info import acalog_client as AcalogClient

from tests.mock_cache import MockCache
from tests.test_data import TestData



TEST_CSV = os.environ.get('TEST_CSV', 'tests/test_data.csv')

TEST_DATA = TestData.read(TEST_CSV)

@pytest.fixture(scope="session")
def db_conn():
    return db

@pytest.fixture(scope="module")
def test_data(db_conn) -> TestData:
    TEST_DATA.clear_db(db_conn)
    TEST_DATA.reload_data(db_conn)

    return TEST_DATA

@pytest.fixture(scope="session")
def class_info(db_conn):
    return ClassInfo(db_conn)

@pytest.fixture(scope="session")
def admin_settings(db_conn):
    return Admin(db_conn)

@pytest.fixture(scope="session")
def semester_info(db_conn):
    return SemesterInfo(db_conn)

@pytest.fixture(scope="session")
def semester_date_mapping(db_conn):
    return SemesterDateMapping(db_conn)

## For future save semester testing
# @pytest.fixture(scope="session")
# def save_semester(db_conn):
# 	return student_course_selection(db_conn)

## For future testing with a user
# @pytest.fixture(scope="session")
# def test_user(db_conn):
# 	return User(db_conn)

@pytest.fixture(scope="session")
def acalog_client():
    acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"
    return AcalogClient(acalog_api_key)

@pytest.fixture(scope="session")
def school_department_mapping():
    file_path = "rpi_data/" + SCHOOL_DEPARTMENT_MAPPING_YAML_FILENAME

    return SchoolDepartmentMapping.parse_yaml(file_path)