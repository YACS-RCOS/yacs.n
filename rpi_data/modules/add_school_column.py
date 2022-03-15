import yaml
import pandas as pd

from typing import List, Dict

# File copied from YACS
SCHOOL_DEPARTMENT_MAPPING_YAML_FILENAME = "school-department-mapping.yaml"
  
class SchoolDepartmentMapping:
  def __init__(self, mapping: Dict[str, str], schools: List[str]):
    """ :param: mapping - dict that maps department shortname -> school longname
                          e.g.  mapping.get('CSCI') == 'Science'
                                mapping.get('COGS') == 'Humanities, Arts and Social Sciences'
        :param: schools - list of schools
    """
    self.mapping = mapping
    self.schools = schools

  def get(self, key: str, default = 'Other') -> str:
    return self.mapping.get(key, default)

  @classmethod
  def parse_yaml(cls, path: str) -> 'SchoolDepartmentMapping':
    data = None

    with open(path) as f:
      data = yaml.safe_load(f.read())

    
    # data is a dict with the following form
    # {
    #   'schools': {
    #     'longname': str ('Humanities, Arts and Social Sciences'),
    #     'subjects': {
    #       'shortname': str ('ARTS'),
    #       'longname: str ('Arts')
    #     }[]
    #   }[]
    # }
    

    mapping: Dict[str, str] = {}

    for school in data['schools']:
      school_longname = school['longname']
      
      for subject in school['subjects']:
        subject_shortname = subject['shortname']

        mapping[subject_shortname] = school_longname

    schools = [school['longname'] for school in data['schools']]
    
    return cls(mapping, schools)

def add_school_column(df: pd.DataFrame, school_department_mapping_path = SCHOOL_DEPARTMENT_MAPPING_YAML_FILENAME) -> pd.DataFrame:
  school_department_mapping = SchoolDepartmentMapping.parse_yaml(school_department_mapping_path)

  df['school'] = df['course_department'].apply(school_department_mapping.get)

  return df