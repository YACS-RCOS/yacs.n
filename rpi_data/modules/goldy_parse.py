import requests
from bs4 import BeautifulSoup as bs

def getGoldyLink(term: str) -> str:
    baseurl = "https://www.cs.rpi.edu/~goldsd/docs/"
    ending = "-topics-courses.txt"
    url = ""
    if term[0:4] == "fall" or term[0:6] == "summer":
        url = baseurl + "u" + str(term[-2:]) + "-f" + str(term[-2:]) + ending
    else:
        if term[0:6] == "spring":
            url = baseurl + "s" + str(term[-2:]) + ending
        else:
            raise ValueError("Incorrect Term Argument")
    return url

def scrapeGoldyLink(link: str) -> dict[str]:
    r = requests.get(link, verify=False)
    soup = bs(r.content, "html.parser")
    parse = soup.text
    
    lines = parse.split("\n")
    course_infos = []
    course = []
    for line in lines:
        if line == "" or "=" in line:
            continue

        if line == '\r':
            if len(course) != 0:
                course_infos.append(course)
                course = []
            continue
        
        course.append(line)
    if (course != []):
        course_infos.append(course)
    terms = []
    term = []
    for s in course_infos:
        if ("U24" in s[0] or "F24" in s[0] or "S24" in s[0]) and "TOPICS" in s[0]:
            if len(term) != 0:
                terms.append(term)
                term = []
            continue
        term.append(s)
    if len(term) != 0:
        terms.append(term)
    return terms






scrapeGoldyLink(getGoldyLink("fall2024"))