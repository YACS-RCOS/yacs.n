import json
from bs4 import BeautifulSoup
import requests

with open('Professors.json') as f:
    data = json.load(f)

#testing html: https://faculty.rpi.edu/kathleen-galloway
#testing html: https://faculty.rpi.edu/keith-fraser

def extract_courses_from_html(url):
    response=requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the teaching header
    teaching_header = soup.find('h2', class_='red sans-alt text-uppercase', string='Teaching')
    
    if not teaching_header:
        return []

    courses = []
    for sibling in teaching_header.find_all_next():
        # If you hit another header, stop
        if sibling.name and sibling.name.startswith('h'):
            break
        # If it's a paragraph, extract the course name
        if sibling.name == 'p':
            text = sibling.text.strip()
            if text:  # To ensure non-empty strings
                courses.append(text)
    print(courses)
    return courses


# testing 
# it work but also scrape the thing beside the course name 
url ="https://faculty.rpi.edu/keith-fraser"
course = extract_courses_from_html(url)
print(course)