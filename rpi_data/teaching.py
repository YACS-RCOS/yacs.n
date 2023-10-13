import json
from bs4 import BeautifulSoup
import requests

with open('Professors.json') as f:
    data = json.load(f)


def extract_courses(soup):
    teachings = {}
    
    teaching_header = soup.find('h2', class_='red')
    
    if not teaching_header:
        return teachings  # return empty dictionary if the header is not found
    
    course_info_div = teaching_header.find_next_sibling('div', class_='field--name-field-teaching-summary')
    if not course_info_div:
        return teachings  # return empty dictionary if the courses div is not found

    categories = course_info_div.select('strong')
    
    for category in categories:
        cat_name = category.text.strip()
        teachings[cat_name] = []

        for sibling in category.find_next_siblings():
            if sibling.name == 'strong':
                break
            if sibling.name == 'p' and sibling.text.strip() != '':
                teachings[cat_name].append(sibling.text.strip())

    return teachings


def scrape_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting titles
    titles_list = soup.select('.doc-title.serif a')
    titles = [title.text.strip() for title in titles_list]
    print(titles)  
    
    # Extracting teaching info
    teachings = extract_courses(soup)
    
    return {
        'titles': titles,
        'teachings': teachings
    }

    
for professor in data:
    profile = professor['Profile Page']

    if profile:
        extracted_data = scrape_info(profile)
        professor['Titles'] = extracted_data['titles']
        professor['Teaching'] = extracted_data['teachings']
    else:
        professor['Teaching'] = 'Not available'

# Save the updated data to new json file
with open('Updated_Professors.json', 'w') as f:
    json.dump(data, f, indent=4)
