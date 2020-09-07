from dataclasses import dataclass
import csv
from datetime import date
import os
import re

from typing import Dict, Set

from src.api.db.semester_info import semester_info as SemesterInfo
from src.api.db.courses import Courses

from tests.mock_cache import MockCache

@dataclass(frozen=True, eq=True)
class Subsemester:
    parent_semester: str
    date_start: str
    date_end: str

    @property
    def date_start_date(self):
        return date(*[int(date_part) for date_part in self.date_start.split("-")])

    @property
    def date_end_date(self):
        return date(*[int(date_part) for date_part in self.date_end.split("-")])

class TestData:
    def __init__(self, filename, course_sessions_by_id, semesters, departments, subsemesters):
        self.filename: str = filename
        self.course_sessions_by_id: Dict[str, dict] = course_sessions_by_id
        self.departments: Set[str] = departments
        self.semesters: Set[str] = semesters
        self.subsemesters: Set[Subsemester] = subsemesters
    
    def clear_db(self, db_conn):
        table_names = []
        for file_name in os.listdir("./src/data/schema"):
            match = re.search("(?<=\d\d_)\w+(?=\.sql)", file_name)
            if match:
                table_names.append(match.group(0))
        
        conn = db_conn.get_connection()
        with conn.cursor() as transaction:
            transaction.execute("TRUNCATE " + ",".join(table_names) + " CASCADE;")
        conn.commit()

    def reload_data(self, db_conn):
        with open(self.filename) as csvfile:
            mock_cache = MockCache()
            for semester in self.semesters:
                SemesterInfo(db_conn).upsert(semester, True)
            courses = Courses(db_conn, mock_cache)
            courses.bulk_delete(self.semesters)
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