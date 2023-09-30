from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR

# from .database import Base
import json


class pathway_field():
    __tablename__ = "pathway_field"

    pathway_name = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    course_name = Column(VARCHAR(length=255), primary_key=True, nullable=False)
    field_number = Column(VARCHAR(length=255), primary_key=False, nullable=False)
    occurrence = Column(VARCHAR(length=255), primary_key=False, nullable=False)
    course_credits = Column(VARCHAR(length=255), primary_key=False, nullable=False)
    desc_credit_level = Column(VARCHAR(length=255), primary_key=False, nullable=True)  # Ex: 12 credits at the...
    desc_course_level = Column(VARCHAR(length=255), primary_key=False, nullable=True)  # Ex: ... 4000 level


if __name__ == "__main__":
    with open('../../web/src/pages/pathwayV2.json') as file:
        data = json.load(file)
    total_keys = set()
    for category in data:
        print('Category:', category["Category Name"][0])
        for pathway in category['Pathways']:
            print('    Pathway:', pathway["Name"][0])
            for key in pathway.keys():
                total_keys.add(key)
                if key != 'Name':
                    print('       ', key + ':')
                    for course in pathway[key]:
                        print('           ', course)
