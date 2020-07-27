from ....rpi_data.modules.add_school_column import SchoolDepartmentMapping, SCHOOL_DEPARTMENT_MAPPING_YAML_FILENAME

school_department_mapping_file_path = "../../../rpi_data/" + SCHOOL_DEPARTMENT_MAPPING_YAML_FILENAME

def test_schools_unique(): 
  mapping = SchoolDepartmentMapping.parse_yaml(school_department_mapping_file_path)

  schools = mapping.schools

  assert len(schools) == len(set(schools))

def test_main_departments():
  mapping = SchoolDepartmentMapping.parse_yaml(school_department_mapping_file_path)

  assert mapping.get("CSCI") == "Science"
  assert mapping.get("BMED") == "Engineering"
  assert mapping.get("ARTS") == "Humanities, Arts, and Social Sciences")