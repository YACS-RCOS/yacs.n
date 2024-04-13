import requests
from bs4 import BeautifulSoup as bs
import json
from lxml import etree

def get_department_links() -> list[str, str]:
    url = "https://faculty.rpi.edu/departments"
    r = requests.get(url)
    f = etree.HTML(r.content)
    L = f.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/div/div/div/ul")[0]
    links = []
    sections = []
    for element in L:
        found_elements = element.findall('.//a')
        section = found_elements[0].text
        for found_element in found_elements:
            links.append(["https://faculty.rpi.edu" + found_element.attrib['href'], section])
    return links

def access_department_links() -> list[str]:
    professors = []
    links_and_sections = get_department_links()
    professor_links_and_sections = []
    for link_section in links_and_sections:
        [professor_links_and_sections.append([i, link_section[1]]) for i in get_professor_links(link_section[0])]


    for link_section in professor_links_and_sections:
        professors.append(scrape_professor_links(link_section[0], link_section[1]))
    
    
    
    print(json.dumps(professors))

    



def get_professor_links(department_link: str) -> list[str]:
    r = requests.get(department_link)
    tree = etree.HTML(r.content)
    page = 0
    found = tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/div/div/div[2]")
    if (len(found) == 0):
        found = tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/div/div/div/div[2]")[0]
    else:
        found = found[0]
    
                       
    unparsed_professor_branches = found
    while len(unparsed_professor_branches) % 25 == 0:
        page += 1
        temp = requests.get(department_link + "?page="+ str(page))
        temp_tree = etree.HTML(temp.content)
        found = temp_tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/div/div/div[2]")
        if len(found) == 0 or "view-empty" in found[0].attrib["class"]:
            break
        found = found[0]
        [unparsed_professor_branches.append(i) for i in found]

    professorlinks = set()    
    
    for element in unparsed_professor_branches:
        stack = []

        stack.append(element)
        result = ""
        
        while len(stack) != 0:
            element_checking = stack.pop()
            if (element_checking.tag == "a"):
                result = element_checking.attrib["href"]
            [stack.append(i) for i in element_checking.getchildren()]
        professorlinks.add(result)
    
    return list(professorlinks)


# We need [Name, Title, Email, Phone, Department, Portfolio, Link]

def scrape_professor_links(link: str, portfolio: str) -> list[str]:
    link = "https://faculty.rpi.edu" + link
    r = requests.get(link)
    tree = etree.HTML(r.content)
    print(link)
    department = tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/article/div/div/div[1]/div[2]/div[1]/div/a")[0].text.strip()
    name = tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[1]/div/h1/span")[0].text.strip()
    title = ""
    title_element = tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/article/div/div/div[1]/div[2]/div[2]/div")
    if (len(title_element) != 0):
        if (len(title_element[0].getchildren()) != 0):
            title = title_element[0].getchildren()[0].text.strip()
        else: 
            title = title_element[0].text.strip()
    
    contact_info = tree.xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/main/section/div[2]/div/article/div/div/div[1]/div[2]/ul")[0]
    li_tags = contact_info.findall('.//li')
    email = ""
    phone_number = ""
    for tag in li_tags:
        i_tag = tag.findall('.//i')[0]
        if (i_tag.attrib['class'] == "far fa-envelope"):
            email = tag.findall('.//a')[0].text.strip()
        if (i_tag.attrib['class'] == "far fa-phone"):
            phone_number = tag.findall('.//a')[0].getchildren()[0].text.replace(".", "-").strip()

    return_dict = {"Name" : name, "Title" : title, "Email" : email, "Phone" : phone_number, "Department" : department, "Portfolio" : portfolio, "Profile Page" : link}
    return return_dict
    
    


access_department_links()