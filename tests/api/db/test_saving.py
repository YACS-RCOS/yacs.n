def test_save_student_courses(save_semester, test_user):
	args = {"name":"Barb", "email":"user1@rpi.edu", "phone":"1234567890", "major":"CS", "password":"123456", "degree":"Undergraduate"}
	args1 = {"name":"Wes", "email":"user2@rpi.edu", "phone":"0123456789", "major":"CS", "password":"246810", "degree":"Undergraduate"}

	uid = test_user.add_user(args)
	uid1 = test_user.add_user(args1)
	print(uid)
	print(uid1)

	(status, err) = save_semester.add_selection('yacs-101', 'FALL 2020', uid, '-1')
	assert(err is None)
	(status1, err) = save_semester.add_selection('yacs-404', 'SPRING 2021', uid, '-1')
	assert(err is None)
	(status2, err) = save_semester.add_selection('rcos', 'FALL 2020', uid1, '-1')
	assert(err is None)
	(status3, err) = save_semester.add_selection('yacs-101', 'FALL 2020', uid, '12345')
	assert(err is None)
	(status4, err) = save_semester.add_selection('yacs-404', 'SPRING 2021', uid, '24680')
	assert(err is None)
	(status5, err) = save_semester.add_selection('rcos', 'FALL 2020', uid1, '12345')
	assert(err is None)
	
	assert(status and status1 and status2 and status3 and status4 and status5)
	(selections, err) = get_selection(uid)
	assert(err is None)
	(selections1, err) = get_selection(uid1)
	assert(err is None)
	
	assert(len(selections) == 4)
	assert(len(selections1) == 2)

	(status, err) = save_semester.remove_selection('rcos', 'FALL 2020', uid1, '12345')
	assert(err is None)
	(status1, err) = save_semester.remove_selection('yacs-404', 'SPRING 2021', uid)
	assert(err is None)

	assert(status and status1)

	(selections, err) = get_selection(uid)
	assert(err is None)
	(selections1, err) = get_selection(uid1)
	assert(err is None)

	assert(len(selections) == 2)
	assert(len(selections1) == 1)
