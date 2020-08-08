
def test_get_classes_full_unique_crns(class_info, test_data):
    (classes_full, err) = class_info.get_classes_full()

    assert err is None
    assert len(classes_full) > 0

    crns = []
    for row in classes_full:
        for section in row['sections']:
            if section and section['crn']:
                crns.append(section['crn'])

    assert len(crns) == len(set(crns))
    

def test_get_classes_full_with_semester_unique_crns(class_info, test_data):
    expected_semester = next(iter(test_data.semesters))

    (classes_full, err) = class_info.get_classes_full(expected_semester)

    assert err is None
    assert len(classes_full) > 0

    crns = []
    for row in classes_full:
        assert expected_semester == row['semester']

        for section in row['sections']:
            if section and section['crn']:
                crns.append(section['crn'])

    assert len(crns) == len(set(crns))

def test_get_departments(class_info, test_data):
    departments, err = class_info.get_departments()
    assert err is None
    assert len(test_data.departments - set(row['department'] for row in departments)) == 0

# def test_get_subsemesters(class_info, test_data):
    
def test_get_semesters(class_info, test_data):
    semesters, err = class_info.get_semesters(True)
    assert err is None
    assert len(test_data.semesters - set(row['semester'] for row in semesters)) == 0

# todo test hidden semesters

# def test_get_all_semester_info(class_info, test_data):

def test_get_classes_by_search_by_department(class_info, test_data):
    expected = next(test_data.course_sessions_iter)
    expected_id = expected['course_crn']
    expected_semester = expected['semester']
    expected_department = expected['course_department']

    classes, err = class_info.get_classes_by_search(semester=expected_semester, search=expected_department)

    assert len(classes) > 0

    for class_row in classes:
        assert expected_semester == class_row['semester']
        assert expected_department == class_row['department']

def test_get_classes_by_search_by_name(class_info, test_data):
    expected = next(test_data.course_sessions_iter)
    expected_semester = expected['semester']
    expected_name = expected['course_name']
    expected_level = int(expected['course_level'])
    expected_department = expected['course_department']

    classes, err = class_info.get_classes_by_search(semester=expected_semester, search=expected_name)

    assert len(classes) == 1

    assert expected_semester == classes[0]['semester']
    assert expected_department == classes[0]['department']
    assert expected_level == classes[0]['level']

def test_get_classes_by_search_by_level(class_info, test_data):
    expected = next(test_data.course_sessions_iter)
    expected_semester = expected['semester']
    expected_level = int(expected['course_level'])

    classes, err = class_info.get_classes_by_search(semester=expected_semester, search=str(expected_level))

    assert len(classes) > 0

    for class_row in classes:
        assert expected_semester == class_row['semester']
        assert expected_level == class_row['level']
    
