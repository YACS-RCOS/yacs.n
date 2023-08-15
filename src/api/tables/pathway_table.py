import json
from .database_session import SessionLocal
from .category import Category
from .pathway import Pathway
from .course import Course

def populate_database():
    with open('pathwayV2.json', 'r') as json_file:
        data = json.load(json_file)

    db = SessionLocal()

    for category_data in data:
        category_name = category_data['Category Name'][0]
        category = Category(name=category_name)
        db.add(category)

        for pathway_data in category_data['Pathways']:
            pathway_name = pathway_data['Name'][0]
            compatible_minors = pathway_data.get('Compatible minor(s)', [])[0]

            pathway = Pathway(id=pathway_name, category_name=category_name, compatible_minors=compatible_minors)
            db.add(pathway)

            for course_name in pathway_data['Choose one of the following'] + pathway_data['Choose remaining credits from the following']:
                course = Course(name=course_name, pathway_id=pathway_name)
                db.add(course)

    db.commit()
    db.close()

if __name__ == "__main__":
    populate_database()
