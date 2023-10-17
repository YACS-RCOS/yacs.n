import json
from bs4 import BeautifulSoup
import requests
import re

def update_all_professors_courses():
    # Load existing data from the JSON file
    with open('Professors.json', 'r') as f:
        data = json.load(f)
    
    # Iterate through each professor and update their "Teaching" field
    for professor in data:
        # Assuming the URL to scrape is in the 'Profile Page' field
        url = professor['Profile Page']
        
        # If there's no URL, skip scraping for this professor
        if not url:
            continue

        courses = extract_courses_from_html(url)
        if courses:
            professor['Teaching'] = ', '.join(courses)
        else:
            professor['Teaching'] = "Not available"

    # Save the updated data back to the JSON file
    with open('Professors.json', 'w') as f:
        json.dump(data, f, indent=4)


#testing html: https://faculty.rpi.edu/kathleen-galloway
#testing html: https://faculty.rpi.edu/keith-fraser
#testing html: https://faculty.rpi.edu/chris-bystroff

def extract_courses_from_html(url):
    response=requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the teaching header or "current course" tage
    teaching_header = soup.find('h2', class_='red sans-alt text-uppercase', string='Teaching')
    current_course_tag = soup.find('strong', string=re.compile("Current Course", re.IGNORECASE))

    startpoint=teaching_header or current_course_tag

    if not startpoint:
        return []

    courses = []
    for sibling in startpoint.find_all_next():
        # If you hit another header, stop
        if sibling.name and sibling.name.startswith('h'):
            break

        # If it's a <strong> tag and not a "Current Course" indicator, consider it a course name
        if sibling.name == 'strong' and sibling.text.strip().lower() != "current course":
            courses.append(sibling.text.strip())
        # If it's a paragraph or a list item, consider it as a potential course title
        elif sibling.name in ['li']:
            text = sibling.text.strip()
            if text:  # To ensure non-empty strings
                courses.append(text)
    return courses


# testing 
# it work but also scrape the thing beside the course name 
# url ="https://faculty.rpi.edu/kathleen-galloway"
# course = extract_courses_from_html(url)
# print(course)
update_all_professors_courses()
