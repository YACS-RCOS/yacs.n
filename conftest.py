import os

import pytest

from src.api.db.connection import db
from src.api.db.classinfo import ClassInfo
from src.api.db.courses import Courses
from src.api.db.admin import Admin
from src.api.db.student_course_selection import student_course_selection
from src.api.db.user import User

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

@pytest.fixture(scope="session")
def save_semester(db_conn):
	return student_course_selection(db_conn)

@pytest.fixture(scope="session")
def test_user():
	return User()

@pytest.fixture(scope="session")
def acalog_client():
    acalog_api_key = "3eef8a28f26fb2bcc514e6f1938929a1f9317628"
    return AcalogClient(acalog_api_key)

if TEST_CSV is not None:
    with open(TEST_CSV) as csvfile:
        Courses(db).populate_from_csv(csvfile)
