# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup


def getFacultyInfo(RCSID: str, session: requests.Session, OriginalName: list = [False]) -> dict:
    '''Parse a single faculty's info and return as a dictionary'''
    html = session.get('https://directory.rpi.edu/pplsearch/NULL/NULL/{}/NULL'
                       .format(RCSID))
    soup = BeautifulSoup(html.text, 'html.parser')
    rawInfo = soup.find_all('div', class_='row p-3 odd')
    # If the faculty is not found, return an empty dict
    # This will deal later in FacultyToJSON
    if len(rawInfo) == 0:
        return {}

    # If the faculty is found, parse the info
    rawInfo = rawInfo[0]
    onePerson = {}

    rawInfo = rawInfo.text
    rawInfo = rawInfo.split('\n')
    for i in range(len(rawInfo)):
        rawInfo[i] = rawInfo[i].strip()
    while '' in rawInfo:
        rawInfo.remove('')

    if OriginalName[0]:
        facultyName = OriginalName[1]
        pass
    else:
        facultyName = rawInfo[0]
    Email = ''
    Phone = ''
    Department = ''
    Portfolio = ''
    Title = rawInfo[1]
    for i in range(len(rawInfo)):
        if rawInfo[i].startswith('Email'):
            Email = rawInfo[i][7:]
        elif rawInfo[i].startswith('Phone'):
            Phone = rawInfo[i][7:]
        elif rawInfo[i].startswith('Department'):
            Department = rawInfo[i+1]
        elif rawInfo[i].startswith('Portfolio'):
            Portfolio = rawInfo[i+1]
    onePerson['Name'] = facultyName
    onePerson['Title'] = Title
    onePerson['Email'] = Email
    onePerson['Phone'] = Phone
    onePerson['Department'] = Department
    onePerson['Portfolio'] = Portfolio
    onePerson['Profile Page'] = verifyProfilePageLink(facultyName)
    return onePerson


def verifyProfilePageLink(facultyName: str) -> str:
    '''Helper function to verify the profile page link is valid or not'''
    link = "https://faculty.rpi.edu/" + \
        facultyName.replace(' ', '-')
    html = requests.get(link)
    if html.status_code == 200:
        return link
    return ""


def FacultyToJSON(AllFaculty: dict, session: requests.Session):
    '''Main function to get all faculty info and write to JSON file'''
    # This is a set to store the RCSID of faculty that is not found
    # So they can be removed from AllFaculty at the end
    PopQueue = set()

    # This is a another way to load data from exsiting JSON file
    # So it might be able to run independently

    # Load Faculty data from JSON file
    # with open("Prof.json", 'r') as infile:
    #     AllFaculty = json.load(infile)
    #     infile.close()

    for RCSID in AllFaculty:
        AllFaculty[RCSID] = getFacultyInfo(RCSID, session)
        if AllFaculty[RCSID] == {}:
            print("Nothing found for this RCSID: " + RCSID)
            PopQueue.add(RCSID)

    for RCSID in PopQueue:
        AllFaculty.pop(RCSID)
        print("Removed: " + RCSID)

    # # Write to JSON file
    with open('Prof.json', 'w') as outfile:
        json.dump(AllFaculty, outfile, indent=4, sort_keys=False)
        outfile.close()
    
    return AllFaculty

def FacultyToList(AllFaculty: dict):
    '''Convert the JSON file to a list'''
    FacultyList = list()

    for RCSID in AllFaculty:
        FacultyList.append(AllFaculty[RCSID])

    # # Write to file
    with open('Prof.txt', 'w') as outfile:
        json.dump(FacultyList, outfile, indent=4, sort_keys=False)
        outfile.close()


if __name__ == "__main__":
    # This would convert the existing JSON file to a list
    with open("Prof.json", 'r') as infile:
        AllFaculty = json.load(infile)
        infile.close()

    FacultyToList(AllFaculty)
