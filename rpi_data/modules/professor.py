import json
from bs4 import BeautifulSoup
import requests
with open('Professors.json') as f:
    data =json.load(f)


def scrape_info(url):
    response =requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    link=soup.find('a',class_='nav-link',text='Teaching')

    if link:
        name=link.text
        print(name)
    else:
        print("not found")
    
    
for professor in data:
    name = professor['Name']
    title = professor['Title']
    email = professor['Email']
    phone =professor['Phone']
    department = professor['Department']
    portfolio  = professor['Portfolio']
    profile = professor['Profile Page']

    if profile:
        classes = scrape_info(profile)
        professor['Teaching']=classes
    else:
        professor['Teaching']='Not available'

'''
save the updated data to new json file
'''
with open('Professors.json','w')as f:
    json.dump(data,f,indent=4)


