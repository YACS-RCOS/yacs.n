from src.api.db.classinfo import ClassInfo
from src.api.db.semester_date_mapping import SemesterDateMapping as SemesterDateMapping
from tests.test_data import TestData

def test_semester_date_mapping_insert(test_data: TestData, semester_date_mapping: SemesterDateMapping, class_info: ClassInfo):
    subsemesters, err = class_info.get_subsemesters()
    assert err is None

    for subsemester in subsemesters:
        assert subsemester['semester_part_name'] is None

    expected_subsemester = next(iter(test_data.subsemesters))
    expected_semester_part_name = "test alias"

    semester_date_mapping.insert(expected_subsemester.date_start, expected_subsemester.date_end, expected_semester_part_name)

    subsemesters, err = class_info.get_subsemesters()
    assert err is None
    
    for subsemester in subsemesters:
        if subsemester['date_start'] == expected_subsemester.date_start_date and subsemester['date_end'] == expected_subsemester.date_end_date:
            assert subsemester['semester_part_name'] == expected_semester_part_name
        else:
            assert subsemester['semester_part_name'] is None

def test_semester_date_mapping_insert_all(db_session, test_data: TestData, semester_date_mapping: SemesterDateMapping, class_info: ClassInfo):
    test_data.clear_db(db_session)
    
    subsemesters, err = class_info.get_subsemesters()
    assert err is None

    for subsemester in subsemesters:
        assert subsemester['semester_part_name'] is None
    
    expected_start_dates = []
    expected_end_dates = []
    expected_semester_part_names = []
    for subsemester in test_data.subsemesters:
        expected_start_dates.append(subsemester.date_start)
        expected_end_dates.append(subsemester.date_end)
        expected_semester_part_names.append(f"{subsemester.date_start} {subsemester.date_end} test alias")

    semester_date_mapping.insert_all(expected_start_dates, expected_end_dates, expected_semester_part_names)

    subsemesters, err = class_info.get_subsemesters()
    assert err is None

    for subsemester in subsemesters:
        expected_index = expected_start_dates.index(str(subsemester['date_start']))

        assert expected_end_dates[expected_index] == str(subsemester['date_end'])
        assert expected_semester_part_names[expected_index] == subsemester['semester_part_name']