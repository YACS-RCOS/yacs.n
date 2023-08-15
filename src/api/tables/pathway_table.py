import json
from .database_session import SessionLocal
from .category import Category
from .pathway import Pathway
from .course import Course

def getPathway(db, course_name):
    pathways = db.query(Pathway).join(Course).filter(Course.name == course_name).all()
    return pathways

def getCourse(db, pathway_name):
    courses = db.query(Course).filter_by(pathway_id=pathway_name).all()
    return courses

def addPathway(db, category_name, pathway_name):
    pathway = Pathway(id=pathway_name, category_name=category_name)
    db.add(pathway)
    db.commit()

def removePathway(db, pathway_name):
    pathway = db.query(Pathway).filter_by(id=pathway_name).first()
    if pathway:
        db.delete(pathway)
        db.commit()

def addCourse(db, course_name, pathway_name):
    course = Course(name=course_name, pathway_id=pathway_name)
    db.add(course)
    db.commit()

def removeCourse(db, course_name, pathway_name):
    course = db.query(Course).filter_by(name=course_name, pathway_id=pathway_name).first()
    if course:
        db.delete(course)
        db.commit()


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

            pathway = Pathway(id=pathway_name, category_name=category_name)
            db.add(pathway)

            for key, courses in pathway_data.items():
                if key.startswith("Choose") or key.startswith("Required"):
                    for course_name in courses:
                        course = Course(name=course_name, pathway_id=pathway_name)
                        db.add(course)
    db.commit()
    db.close()

if __name__ == "__main__":
    populate_database()
