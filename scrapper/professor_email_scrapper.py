import requests
from bs4 import BeautifulSoup
import json

url = 'http://catalog.rpi.edu/content.php?catoid=24&navoid=609'
response = requests.get(url)

if response.status_code == 200:
    list = []
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    name_tags = soup.select('p strong')
    i = 0
    for name_tag in name_tags:
        name = name_tag.get_text()
        list.append([])
        list[i].append(name.replace(',','').strip('*').strip('†').split(' '))
        i += 1
else:
    print('Failed to retrieve HTML')

list.remove([['Faculty', 'Roster']])
for i in list:
    if i == [['‘']] or i == [['\xa0']]:
        list.remove(i)
print(list)
i = 0
email_list = []
j = 0
print(len(list))
professor_dict = []
for i in list:
    professor = i[0][1]+'-'+i[0][0]
    professor_url = 'https://faculty.rpi.edu/' + professor
    response_professor = requests.get(professor_url)
    if response_professor.status_code == 200:
        html2 = response_professor.text
        soup2 = BeautifulSoup(html2, 'html.parser')
        email_address = soup2.select_one('a[href^="mailto:"]').get('href').replace("mailto:", "")
        new_dict = {professor:email_address}
        professor_dict.append(new_dict)
with open("email.json", "w") as outfile:
    json.dump(professor_dict,outfile, indent=1)


