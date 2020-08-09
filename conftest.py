import os
from dataclasses import dataclass
from datetime import date
from typing import List, Set, Dict, Tuple

import pytest
import csv

from src.api.db.connection import db
from src.api.db.classinfo import ClassInfo
from src.api.db.courses import Courses
from src.api.db.admin import Admin
from src.api.db.semester_info import semester_info as SemesterInfo
# from src.api.db.student_course_selection import student_course_selection
# from src.api.db.user import User
from rpi_data.modules.add_school_column import SchoolDepartmentMapping, SCHOOL_DEPARTMENT_MAPPING_YAML_FILENAME
from rpi_data.modules.fetch_catalog_course_info import acalog_client as AcalogClient

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

@dataclass(frozen=True, eq=True)
class Subsemester:
    parent_semester: str
    start_date: str
    end_date: str

class TestData:
    def __init__(self, filename, course_sessions_by_id, semesters, departments, subsemesters):
        self.filename: str = filename
        self.course_sessions_by_id: Dict[str, dict] = course_sessions_by_id
        self.departments: Set[str] = departments
        self.semesters: Set[str] = semesters
        self.subsemesters: Set[Subsemester] = subsemesters

    def reload_db(self, db_conn):
        with open(self.filename) as csvfile:
            mock_cache = MockCache()
            for semester in self.semesters:
                SemesterInfo(db_conn).upsert(semester, True)
            courses = Courses(db_conn, mock_cache)
            courses.bulk_delete(TEST_DATA.semesters)
            courses.populate_from_csv(csvfile)
            assert(mock_cache.cache_cleared)
    
    @property
    def course_sessions_iter(self):
        return iter(self.course_sessions_by_id.values())

    @classmethod
    def read(cls, filename):
        with open(filename) as f:
            reader = csv.DictReader(f)

            course_sessions_by_id: Dict[str, dict] = {}
            semesters: Set[str] = set()
            departments: Set[str] = set()
            subsemesters: Set[Subsemester] = set()
            
            for row in reader:
                course_sessions_by_id[row['course_crn']] = row

                semesters.add(row['semester'])
                departments.add(row['course_department'])
                subsemesters.add(Subsemester(row['semester'], row['course_start_date'], row['course_end_date']))

            return cls(filename, course_sessions_by_id, semesters, departments, subsemesters)


TEST_CSV = os.environ.get('TEST_CSV', 'tests/test_data.csv')

TEST_DATA = TestData.read(TEST_CSV)

@pytest.fixture(scope="session")
def db_conn():
    return db

@pytest.fixture(scope="module")
def test_data(db_conn) -> TestData:
    TEST_DATA.reload_db(db_conn)

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