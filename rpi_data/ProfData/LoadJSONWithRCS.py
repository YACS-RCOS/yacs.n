# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup


def parseHtmlToGetFacultyEmail(soup: BeautifulSoup) -> dict:
    '''Parse the soup to get faculty email(s)'''
    Faculty = {}
    links = soup.find_all('a', href=True)
    for link in links:
        if link['href'].startswith('mailto:'):
            Faculty[link['href'][7:]] = link['target']
    return Faculty


def parseRCSID(Faculty: dict) -> list:
    '''Helper function to parse the RCSID(s) from the email dictionary'''
    RCSIDs = [email.split('@')[0] for email in Faculty]
    return RCSIDs


def loadCourseTreeWithRCSID(CourseTree: dict, AllFaculty: dict, session: requests.Session):
    '''Fill each course with the RCSID(s) of the faculty'''
    for semester in CourseTree:
        for department in CourseTree[semester]:
            for course in CourseTree[semester][department]:
                for crn in CourseTree[semester][department][course]:
                    link = getCourseLink(semester, department, course, crn)
                    html = session.get(link)
                    soup = BeautifulSoup(html.text, 'html.parser')
                    facultys = parseHtmlToGetFacultyEmail(soup)
                    RCSIDs = parseRCSID(facultys)
                    CourseTree[semester][department][course][crn] = RCSIDs
                    for RCSID in RCSIDs:
                        AllFaculty[RCSID] = {}


def getCourseLink(semester: str, department: str, course: str, crn: str) -> str:
    '''Helper function to get the link of the course'''
    link = 'https://sis.rpi.edu/rss/bwckschd.p_disp_listcrse\
?term_in={}&subj_in={}&crse_in={}&crn_in={}'.format(
        semester, department, course, crn)
    return link


def FillJSONWithRCSIDs(session) -> dict:
    '''Main function to fill the JSON file with RCSIDs'''
    Courses = dict()
    AllFaculty = dict()

    # Load course data from JSON file
    with open("Courses.json", 'r') as infile:
        Courses = json.load(infile)
        infile.close()

    loadCourseTreeWithRCSID(Courses, AllFaculty, session)

    # Write to JSON file
    with open("Courses.json", 'w') as outfile:
        json.dump(Courses, outfile, indent=4, sort_keys=False)
        outfile.close()

    # If we need to run this script indpendently, uncomment the following code
    # In that way, we can also run getAllFacultyToJSON.py independently
    # with open("Prof.json", 'w') as outfile:
    #     json.dump(AllFaculty, outfile, indent=4, sort_keys=True)

    return AllFaculty


if __name__ == "__main__":
    # This code can be run independently if and only if 
    # the code in FillJSONWithRCSIDs is uncommented
    # session = requests.Session()
    # FillJSONWithRCSIDs(session)
    pass
