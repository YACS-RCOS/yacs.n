def test_get_default_semester(admin_settings):
    default_semester = admin_settings.get_semester_default()
    print(default_semester)
    assert(isinstance(default_semester, str) or default_semester is None)