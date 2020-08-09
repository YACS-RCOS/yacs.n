def test_default_semester(admin_settings):
    default_semester, error = admin_settings.get_semester_default()
    assert(error is None)
    assert default_semester is None

    expected_semester = "SEMESTER"
    completed, error = admin_settings.set_semester_default(expected_semester)
    assert error is None
    assert True == completed

    default_semester, error = admin_settings.get_semester_default()
    assert error is None
    assert expected_semester == default_semester
