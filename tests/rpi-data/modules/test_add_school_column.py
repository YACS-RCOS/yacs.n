def test_schools_unique(school_department_mapping): 
  schools = school_department_mapping.schools

  assert len(schools) == len(set(schools))

def test_main_departments(school_department_mapping):
  assert school_department_mapping.get("CSCI") == "Science"
  assert school_department_mapping.get("BMED") == "Engineering"
  assert school_department_mapping.get("ARTS") == "Humanities, Arts and Social Sciences"