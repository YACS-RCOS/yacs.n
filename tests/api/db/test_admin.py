def test_get_default_semester(admin_settings):
    default_semester, error = admin_settings.get_semester_default()
    assert(error is None)
    assert(isinstance(default_semester, str) or default_semester is None)
