import os

import pytest

from src.db.connection import db
from src.db.classinfo import ClassInfo

@pytest.fixture(scope="session")
def db_conn():
    return db

@pytest.fixture(scope="session")
def class_info(db_conn):
    return ClassInfo(db_conn)