def test_get_classes_full_unique_crns(class_info):
    (classes_full, err) = class_info.get_classes_full()

    assert err is None
    assert len(classes_full) > 0

    crns = []
    for row in classes_full:
        for section in row['sections']:
            if section and section['crn']:
                crns.append(section['crn'])

    assert len(crns) == len(set(crns))

def test_get_classes_full_with_semester_unique_crns(class_info):
    (classes_full, err) = class_info.get_classes_full()

    assert err is None
    assert len(classes_full) > 0

    crns = []
    for row in classes_full:
        for section in row['sections']:
            if section and section['crn']:
                crns.append(section['crn'])

    assert len(crns) == len(set(crns))
    

def test_get_classes_by_search(class_info, test_data):
    expected = next(test_data.course_sessions_iter)
    expected_id = expected['course_crn']
    expected_semester = expected['semester']
    expected_department = expected['course_department']

    # search by department
    classes, err = class_info.get_classes_by_search(semester=expected_semester, search=expected_department)

    assert len(classes) > 0

    for class_row in classes:
        assert expected_semester == class_row['semester']
        assert expected_department == class_row['department']

    expected_name = expected['course_name']

    # search by name
    classes, err = class_info.get_classes_by_search(semester=expected_semester, search=expected_name)

    assert len(classes) > 0
    print(classes[0])
    assert expected_id == classes[0]['crn']

    for class_row in classes:
        assert expected_semester == class_row['semester']

    # search by level




    
