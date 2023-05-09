# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup

departments = ["ARTS", "COGS", "STSH", "STSS", "COMM", "ECON", "GSAS", "IHSS",
               "LANG", "LITR", "PHIL", "PSYC", "WRIT", "BMED", "CHME", "ECSE",
               "ENVE", "MANE", "MTLE", "CIVL", "ENGR", "ESCI", "ISYE", "EPOW",
               "BCBP", "CSCI", "ERTH", "IENV", "ISCI", "MATP", "PHYS", "ASTR",
               "BIOL", "CHEM", "MATH", "ITWS", "ARCH", "LGHT", "MGMT", "ADMN",
               "USAF", "USNA", "USAR"]


def getAllLink(soup: BeautifulSoup) -> list:
    '''Helper function to get all the links from the soup'''
    rawLinks = soup.find_all('a', href=True)
    returnLinks = []
    for link in rawLinks:
        if link['href'].startswith("/rss/bwckctlg.p_disp_listcrse"):
            returnLinks.append("https://sis.rpi.edu" + link['href'])
    return returnLinks


def parseCRNs(link: str, session) -> list:
    '''Helper function get CRNs from the link page'''
    html = session.get(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    rawCRNs = soup.find_all('a', href=True)
    CRNs = []
    for CRN in rawCRNs:
        if CRN['href'].startswith("/rss/bwckschd.p_disp_detail_sched"):
            CRNs.append(CRN['href'].split('crn_in=')[1])
    return CRNs


def CreateCoursesTree(Tree: dict, semester: str, department: str, course: str, CRNs: list) -> None:
    '''Helper function to construct the tree'''
    if semester not in Tree:
        Tree[semester] = dict()
    if department not in Tree[semester]:
        Tree[semester][department] = dict()
    if course not in Tree[semester][department]:
        Tree[semester][department][course] = dict()
    for crn in CRNs:
        Tree[semester][department][course][crn] = []
    return None


def getAllCourses(departments: list, session, YearAndSemester: str):
    '''Main function to get all the courses'''
    courseTree = dict()
    for department in departments:
        link = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in={}&call_proc_in\
=&sel_subj=&sel_levl=&sel_schd=&sel_coll\
=&sel_divs=&sel_dept=&sel_attr=&sel_subj={}".format(YearAndSemester, department)
        html = session.get(link)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'html.parser')
            linksInDepartment = getAllLink(soup)
            for link in linksInDepartment:
                CRNs = parseCRNs(link, session)
                CreateCoursesTree(courseTree, YearAndSemester,
                                  department, link.split('?')[1].split('&')[2].split('=')[1], CRNs)
        else:
            print("department: {} not found".format(department))
    return courseTree


def CreateCoursesJSON(session=None, YearAndSemester: str = "202305"):
    '''Main function to parse data and create the JSON file'''
    if session == None:
        session = requests.Session()
    courseTree = getAllCourses(departments, session, YearAndSemester)

    with open('Course.json', 'w') as outfile:
        json.dump(courseTree, outfile, indent=4, sort_keys=False)
        outfile.close()

    return courseTree


if __name__ == "__main__":
    # This code can always run independently
    # TODO: add option to set semester, and find a way to get all the departments
    # Also need error handling
    CreateCoursesJSON()
