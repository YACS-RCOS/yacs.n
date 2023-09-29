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
    for category in data:
        print('Category Name:', category["Category Name"][0])
        print('  Pathways:')
        for pathway in category['Pathways']:
            print('   ', pathway["Name"][0])
            if 'Choose one of the following' in pathway.keys():
                print('      Choose one of the following:')
                for course in pathway['Choose one of the following']:
                    print('       ', course)
            if 'Choose remaining credits from the following' in pathway.keys():
                print('      Choose remaining credits from the following:')
                for course in pathway['Choose remaining credits from the following']:
                    print('       ', course)
            if 'Choose 12 credits from the following, with at least 4 credits at the 4000-level' in pathway.keys():
                print('      Choose 12 credits from the following, with at least 4 credits at the 4000-level:')
                for course in pathway['Choose 12 credits from the following, with at least 4 credits at the 4000-level']:
                    print('       ', course)
