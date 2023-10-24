from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

# from .database import Base
import json


class Pathway_Field():
    __tablename__ = "pathway_field"

    pathway_name = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    course_name = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    field_name = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    occurrence = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    course_credits = Column(VARCHAR(length=255), primary_key=False, nullable=False)
    desc_credit_level = Column(VARCHAR(length=255), primary_key=False, nullable=True)  # Ex: 12 credits at the...
    desc_course_level = Column(VARCHAR(length=255), primary_key=False, nullable=True)  # Ex: ... 4000 level


def printPathways(data):
    for entry in data:
        for sub in entry['Pathways']:
            for key in sub.keys():
                if key != 'Name' and key != 'Compatible minor(s)':
                    for course in sub[key]:
                        print(course)
                        d_code = ''
                        c_code = ''
                        c_name = ''
                        tokens = course.split('-')
                        if len(tokens) == 1:
                            print(tokens[0])
                            tokens = tokens[0].split()
                            d_code = tokens[0]
                            c_code = tokens[1]
                        else:
                            dept_and_code = tokens[0].split()
                            d_code = dept_and_code[0]
                            c_code = dept_and_code[1]
                            c_name = tokens[1].strip()
                        print('"' + d_code + '", "' + c_code + '", "' + c_name + '"')
                        print()

def printKeys(data):
    total_keys = set()
    print('Keys:')
    for category in data:
        for pathway in category['Pathways']:
            for key in pathway.keys():
                total_keys.add(key)
    for key in sorted(total_keys):
        print(' ', key)


def loadFields(fields):
    fields.clear()
    fields['Choose one'] = list()
    fields['Choose one'].append('Choose one of the following')
    fields['Choose one'].append('Choose another one of the following')
    fields['Choose x'] = list()
    fields['Choose x'].append('Choose 12 credits from the following')
    fields['Choose x'].append('Choose 12 credits from the following course prefixes, with at least 8 credit hours at, or above, the 2000-level and at least 3 credit hours at the 4000-level')
    fields['Choose x'].append('Choose 12 credits from the following, with at least 4 credits at the 4000-level')
    fields['Choose x'].append('Choose 4 credits from the following')
    fields['Choose remaining'] = list()
    fields['Choose remaining'].append('Choose remaining credits from the following')
    fields['Choose remaining'].append('Choose remaining credits from the following, with at least 4 credits at the 4000-level')
    fields['Required'] = list()
    fields['Required'].append('Required')


# if __name__ == "__main__":
#     with open('../../web/src/pages/pathwayV2.json') as file:
#         data = json.load(file)
#     printKeys(data)
#     fields = dict()
#     loadFields(fields)
#
#     # for i in data:
#     #     for j in i['Pathways']:
#     #         print(j["Name"][0], "     ", i['Category Name'][0])
#
#     printPathways(data)
