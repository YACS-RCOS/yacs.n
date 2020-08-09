def test_semester_info(semester_info, test_data):
    for semester in test_data.semesters:
        assert True == semester_info.is_public(semester)

    expected_public_semester = next(iter(test_data.semesters))
    semester_info.upsert(expected_public_semester, False)

    for semester in test_data.semesters:
        assert (semester != expected_public_semester) == semester_info.is_public(semester)

    semester_info.upsert(expected_public_semester, True)

    for semester in test_data.semesters:
        assert True == semester_info.is_public(semester)