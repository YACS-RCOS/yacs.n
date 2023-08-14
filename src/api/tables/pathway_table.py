import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from category import Category
from pathway import Pathway
from course import Course
from database import Base

# Load JSON data
with open('pathwayV2.json', 'r') as json_file:
    data = json.load(json_file)

# Create a database connection
engine = create_engine('your_database_connection_string')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Iterate through JSON data and populate the database
for item in data:
    category = Category(name=item['Category Name'][0])
    session.add(category)
    
    for pathway_data in item['Pathways']:
        pathway = Pathway(name=pathway_data['Name'][0], category=category)
        session.add(pathway)
        
        for course_name in pathway_data['Choose one of the following']:
            course = Course(title=course_name, pathway=pathway)
            session.add(course)
    
    session.commit()
