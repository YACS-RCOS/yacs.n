import os

import pytest

from src.api.db.connection import db
from src.api.db.classinfo import ClassInfo
from src.api.db.courses import Courses
from src.api.db.admin import Admin
# from src.api.db.student_course_selection import student_course_selection
# from src.api.db.user import User
from rpi_data.modules.add_school_column import SchoolDepartmentMapping, SCHOOL_DEPARTMENT_MAPPING_YAML_FILENAME


class MockCache:
    """simple cache mock"""
    def __init__(self):
        self.__reset()

    def clear(self):
        self.cache_cleared = True

    def __is_cleared(self):
        return self.cache_cleared

    def __reset(self):
        self.cache_cleared = True


from rpi_data.modules.fetch_catalog_course_info import acalog_client as AcalogClient

TEST_CSV = os.environ.get('TEST_CSV', None)

@pytest.fixture(scope="session")
def db_conn():
    return db


@pytest.fixture(scope="session")
def class_info(db_conn):
    return ClassInfo(db_conn)

@pytest.fixture(scope="session")
def admin_settings(db_conn):
    return Admin(db_conn)

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

if TEST_CSV is not None:
    with open(TEST_CSV) as csvfile:
        mock_cache = MockCache()
        Courses(db, mock_cache).populate_from_csv(csvfile)
        assert(mock_cache.cache_cleared)
