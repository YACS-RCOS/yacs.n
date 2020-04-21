def test_save_student_courses(save_semester):
	(status, err) = save_semester.add_selection('yacs-101', 'FALL 2020', '21', '-1')
	assert(err is None)
    (status1, err) = save_semester.add_selection('yacs-404', 'SPRING 2021', '21', '-1')
    assert(err is None)
    (status2, err) = save_semester.add_selection('rcos', 'FALL 2020', '42', '-1')
    assert(err is None)
    (status3, err) = save_semester.add_selection('yacs-101', 'FALL 2020', '21', '12345')
    assert(err is None)
    (status4, err) = save_semester.add_selection('yacs-404', 'SPRING 2021', '21', '24680')
    assert(err is None)
    (status5, err) = save_semester.add_selection('rcos', 'FALL 2020', '42', '12345')
    assert(err is None)

    assert(status and status1 and status2 and status3 and status4 and status5)

    (selections, err) = get_selection('21')
    assert(err is None)
    (selections1, err) = get_selection('42')
    assert(err is None)

    assert(len(selections) == 4)
    assert(len(selections1) == 2)
    