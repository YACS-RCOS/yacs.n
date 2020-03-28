import os

import pytest

from src.db.connection import db
from src.db.classinfo import ClassInfo
from src.db.courses import Courses

TEST_CSV = os.environ.get('TEST_CSV', None)

@pytest.fixture(scope="session")
def db_conn():
    return db

@pytest.fixture(scope="session")
def class_info(db_conn):
    return ClassInfo(db_conn)

if TEST_CSV is not None:
    with open(TEST_CSV) as csvfile:
        Courses(db).populate_from_csv(csvfile)
