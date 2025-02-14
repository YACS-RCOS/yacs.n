from regex import P
import requests
from bs4 import BeautifulSoup as bs
import csv
'''
Turns a trerm into a valid link for Professor Goldschmidt's course information
'''
def get_goldy_link(term: str) -> str:
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

'''
Scrapes the course information from the given link by splitting by term and then splits by line to get each individual course.
'''
def scrape_goldy_link(link: str) -> list[list[list[str]]]:
    r = requests.get(link, verify=False)
    soup = bs(r.content, "html.parser")
    parse = soup.text
    
    lines = parse.split("\n")
    course_infos = []
    course = []
    for line in lines:
        if line == "" or "======" in line:
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

'''
Parent function that gets the course information from the given term and then parses the course info into a dictionary.
'''
def get_goldy_info(term: str) -> list[dict[str]]:
    requests.packages.urllib3.disable_warnings() # ignore HTTP warnings
    url = get_goldy_link(term)
    terms_list = scrape_goldy_link(url)
    scraped_list = []
    if ("fall" in term):
        scraped_list = terms_list[1]
    else:
        scraped_list = terms_list[0]
    named_dict = dict()
    for course in scraped_list:
        course_dict = dict()
       
        for info in course:
            pair = info.split(":")
            if (len(pair) == 1):
                course_dict["Name"]  = pair[0].strip()
            else:
                temp_string = ""
                for i in range(1, len(pair)):
                    temp_string += pair[i]
                course_dict[pair[0]] = temp_string.strip()
        name_split = course_dict["Name"].split(" ")
        major = name_split[0]
        codes = name_split[1]
        course_dict["Name"] = course_dict["Name"].replace(major, "").replace(codes, "").strip()
        for code in codes.split("/"):
            named_dict[major + " " + code] = course_dict
    
    return named_dict

if __name__ == "__main__":
    print(get_goldy_info("fall2024"))