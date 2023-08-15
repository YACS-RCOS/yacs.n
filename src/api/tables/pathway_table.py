import json
from connection import db
from category import Category
from pathways import Pathway
from course import Course

def create_category(name):
    return Category(name=name)

def create_pathway(name, category):
    return Pathway(name=name, category=category)

def create_course(name, pathway):
    return Course(name=name, pathway=pathway)

def populate_database(data):
    for entry in data:
        category_name = entry["Category Name"][0]
        category = create_category(category_name)

        for pathway_data in entry["Pathways"]:
            pathway_name = pathway_data["Name"][0]
            pathway = create_pathway(pathway_name, category)

            for key, value in pathway_data.items():
                if isinstance(value, list) and all(isinstance(course_name, str) for course_name in value):
                    for course_name in value:
                        course = create_course(course_name, pathway)
                        db.execute("INSERT INTO courses (name, pathway_id) VALUES (%s, %s)", (course.name, course.pathway_id), isSELECT=False)

    db.close()

if __name__ == "__main__":
    with open("pathwayV2.json", "r") as json_file:
        data = json.load(json_file)
        populate_database(data)
