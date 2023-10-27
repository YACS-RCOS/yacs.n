import json
from bs4 import BeautifulSoup
import requests
import re 

with open('Professors.json') as f:
    data =json.load(f)
def scrape_info(url):
    response =requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    titles_list = soup.select('.doc-title.serif a')
    titles = [title.text.strip() for title in titles_list]
    print(titles)  
    if not link:
        return None
    teaching_url = link['href'] if link.has_attr('href') else None
    if not teaching_url:
        return None
    response = requests.get(teaching_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # extract the classes. The exact method will depend on the structure of the webpage.
    classes_list = soup.find_all('li', class_='class-item')
    #classes = [item.text for item in classes_list]
    pattern = re.compile(r'[A-Z]+\s\d{4} - [A-Za-z\s]+')
    classes = [re.search(pattern, item.text).group() for item in classes_list if re.search(pattern, item.text)]
    return classes
for professor in data:
    name = professor['Name']
    title = professor['Title']
    email = professor['Email']
    phone =professor['Phone']
    department = professor['Department']
    portfolio=professor['Portfolio']
    profile = professor['Profile Page']
    if profile:
        classes = scrape_info(profile)
        professor['Teaching'] = classes if classes else 'Not available'
    else:
        professor['Teaching'] = 'Not available'
'''
save the updated data to new json file
'''
with open('Professors.json','w')as f:
    json.dump(data,f,indent=4)


