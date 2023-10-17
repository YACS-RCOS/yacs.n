import json
from bs4 import BeautifulSoup
import requests
import re

with open('Professors.json') as f:
    data = json.load(f)

#testing html: https://faculty.rpi.edu/kathleen-galloway
#testing html: https://faculty.rpi.edu/keith-fraser
#testing html: https://faculty.rpi.edu/chris-bystroff

def extract_courses_from_html(url):
    response=requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the teaching header
    teaching_header = soup.find('h2', class_='red sans-alt text-uppercase', string='Teaching')
    
    if not teaching_header:
        return []

    courses = []
    for strong_tag in teaching_header.find_all_next('strong'):
        # If you hit another header, stop
        if any(sibling.name and sibling.name.startswith('h') for sibling in strong_tag.find_next_siblings(limit =1)):
            break
        courses.append(strong_tag.text.strip())
    return courses


# testing 
# it work but also scrape the thing beside the course name 
url ="https://faculty.rpi.edu/kathleen-galloway"
course = extract_courses_from_html(url)
print(course)