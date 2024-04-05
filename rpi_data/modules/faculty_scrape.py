import requests
from bs4 import BeautifulSoup as bs
import json
from lxml import etree

def get_department_links() -> list[str]:
    url = "https://faculty.rpi.edu/departments"
    r = requests.get(url)
    f = etree.HTML(r.content)
    L = f.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/div/div/div/ul")[0]
    links = []
    for element in L:
        found_elements = element.findall('.//a')
        for found_element in found_elements:
            links.append("https://faculty.rpi.edu" + found_element.attrib['href'])
    return links

def access_department_links() -> list[str]:
    links = get_department_links()
    for link in links:
        get_professor_links(link)

def get_professor_links(department_link: str):
    r = requests.get(department_link)
    tree = etree.HTML(r.content)
    page = 0
    found = tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/div/div/div[2]")[0]
    unparsed_professor_branches = found
    while len(unparsed_professor_branches) % 25 == 0:
        page += 1
        temp = requests.get(department_link + "?page="+ str(page))
        temp_tree = etree.HTML(temp.content)
        found = temp_tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/div/div/div[2]")
        if len(found) == 0:
            break
        found = found[0]
        [unparsed_professor_branches.append(i) for i in found]


access_department_links()