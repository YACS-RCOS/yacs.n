def test_get_classes_full(class_info):
    (classes_full, err) = class_info.get_classes_full()

    crns = []
    for row in classes_full:
        for section in row['sections']:
            if section and section['crn']:
                crns.append(section['crn'])

    assert len(crns) == len(set(crns))
    assert False

def test_get_classes_by_search(class_info):
    (classes, err) = class_info.get_classes_by_search(semester="FALL 2020", search="CSCI")
    assert len(classes) >= 0
    for class_row in classes:
        assert class_row.semester == "FALL 2020"
        assert class_row.department == "CSCI"
