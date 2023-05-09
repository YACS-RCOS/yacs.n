# GOAL: fix description and pre/co-requisites for courses
# Target URL: https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in=202209&subj_code_in=CSCI&crse_numb_in=2500
# TODO: remove \n \n in description

import os
import requests
import json
from bs4 import BeautifulSoup
import csv
import re

baseLink = 'https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={semester}&\
subj_code_in={department}&crse_numb_in={courseNumber}'


def read_csv(file_name : str = 'fall-2023.csv') -> list:
    with open(file_name, 'r', encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_reader = list(csv_reader)
        csv_reader.pop(0)
        return csv_reader

def write_csv(file_name : str = 'fall-2023_fixed.csv', data :list = []) -> None:
    with open(file_name, 'w', encoding='UTF-8') as csv_file:
        data.insert(0,['course_name', 'course_type', 'course_credit_hours', 
        'course_days_of_the_week', 'course_start_time', 'course_end_time', 
        'course_instructor', 'course_location', 'course_max_enroll', 'course_enrolled', 
        'course_remained', 'course_department', 'course_start_date', 'course_end_date', 
        'semester', 'course_crn', 'course_level', 'course_section', 'short_name', 'full_name', 
        'description', 'raw_precoreqs', 'offer_frequency', 'prerequisites', 'corequisites', 
        'school'])
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

def parsePrerequisites(rawPrerequisites : str) -> str:
    if rawPrerequisites == 'None':
        return None
    retList = []
    for item in re.findall(r'\b[A-Z]{4}\s\d{4}\b', rawPrerequisites):
        retList.append(item.replace(' ','-'))
    return retList

def parseCorequisites(rawCorequisites : str) -> str:
    if rawCorequisites == 'None':
        return None
    retList = []
    for item in re.findall(r'\b[A-Z]{4}\s\d{4}\b', rawCorequisites):
        retList.append(item.replace(' ','-'))
    return retList

def readData(filename : str) -> dict:
    with open(filename, 'r', encoding='UTF-8') as infile:
        return json.load(infile)

def saveData(filename :str, data : dict) -> None:
    with open(filename, 'w', encoding='UTF-8') as outfile:
        json.dump(data, outfile, indent=4)
    return None

def getCourseLink(semester : str, department : str, courseNumber : str) -> str:
    return baseLink.format(semester=semester, department=department, courseNumber=courseNumber)

def WithoutData(filename : str, dataFilename : str, DEBUG):
    session = requests.Session()
    data = read_csv(filename)
    semester = parseSemester(filename)
    Data = dict()

    for row in data:
        department = row[11]
        courseNumber = row[16]
        link = getCourseLink(semester, department, courseNumber)
        if DEBUG == 'y':
            print(link)
        page = session.get(link)
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
        rawbody = soup.find('td', class_='ntdefault')
        body = rawbody.text.split('\n\n')
        description = body[0].strip()
        description = description.split('\n \n')[0]
        description = description.replace('\n','')
        
        prerequisites = None
        corequisites = None
        for i in range(1,len(body)):
            if body[i].strip() == 'Prerequisites:':
                rawprerequisites = parsePrerequisites(body[i+1].strip())
                if rawprerequisites != []:
                    prerequisites = rawprerequisites
            if body[i].strip() == 'Corequisites:':
                rawcorequisites = parseCorequisites(body[i+1].strip())
                if rawcorequisites != []:
                    corequisites = rawcorequisites
        row[20] = description
        if prerequisites != None:
            row[23] = prerequisites
        if corequisites != None:
            row[24] = corequisites
        shortName = department+courseNumber
        Data[shortName] = dict()
        Data[shortName]['description'] = description
        Data[shortName]['prerequisites'] = prerequisites
        Data[shortName]['corequisites'] = corequisites
    write_csv(filename,data)
    saveData(dataFilename, Data)

def WithData(filename : str, dataFilename : str) -> None:
    Data = readData(dataFilename)
    data = read_csv(filename)
    for row in data:
        department = row[11]
        courseNumber = row[16]
        shortName = department+courseNumber
        if shortName not in Data:
            WithoutData(filename, dataFilename, 'n')
            return None
        description = Data[shortName]['description']
        prerequisites = Data[shortName]['prerequisites']
        corequisites = Data[shortName]['corequisites']
        row[20] = description
        if prerequisites != None:
            row[23] = prerequisites
        if corequisites != None:
            row[24] = corequisites
    write_csv(filename,data)
    # saveData(dataFilename, Data)

def parseSemester(filename) -> str:
    semester = filename.split('.')[0]
    season, year = semester.split('-')
    if season == 'fall':
        season = '09'
    elif season == 'spring':
        season = '01'
    elif season == 'arch':
        season = '05'
    elif season == 'winter':
        season = '12'
    return year+season
    

def main() -> None:
    filename = os.environ.get('TARGET_FILE')
    dataFilename = os.environ.get('DATA_FILE')
    hasData = os.environ.get('HAS_DATA')
    DEBUG = os.environ.get('DEBUG')

    # # rpi_data/modules/fall-2023.csv
    # filename = input("Input filename: ")
    # # rpi_data/modules/data.json
    # dataFilename = input("Input data filename: ")
    # # y
    # hasData = input("with data? (y/n): ").strip().lower()

    if hasData == 'y':
        WithData(filename, dataFilename)
    else:
        semester = parseSemester(filename)
        WithoutData(filename, dataFilename, DEBUG)


if __name__ == '__main__':
    main()