# WHAT THIS FILE DOES
# This file creates a CSV file that contains course data of all classes offered during the semester
# The name of the file will always follow the format: {semester}-{year}.csv  (e.g. summer-2023.csv)
# Data contained in this CSV file is exactly same as the information users see on the YACS website.
# 
# 
# HOW TO RUN/DEBUG:
# In order to run this file and create the csv file, run the corresponding update bash file. 
# The command line for running the bash file is simply ./update-{semeester}-{year}.sh 
# For example, if you want to update the values for classes in summer 2023, run ./update-summer-2023.sh on linux
# 
# using print() will print directly on the terminal
# 
# SETTING UP ENVIRONMENT VARIABLES:
# The following envrionment variables are already set for you,
#   DATA_FILE=summer-2023_data.json ; The cache filename
#   TARGET_FILE=summer-2023.csv     ; The file to prosses
#   HAS_DATA=y                      ; y if has the cache file, n otherwise
#   DEBUG=n                         ; y if need debug info, n otherwise
#
# ... but you can change them as needed in the update bash file
#
# FINDING THE LINK TO EXTRACT DATA FROM:
# The link that contains information of each course has the format of 'https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={semester}&subj_code_in={department}&crse_numb_in={courseNumber}'
# 
# semesester is a concatenation of the year and season. Season is based on the month the semesester starts in and is one of the following: '09',  '01',  '05', '12'.
#   So fall 2021 would be '202109' and summer 2023 would be '202305'
# department is a four-letter string. ('CSCI' or 'ARTS')
# courseNumber is a four-digit number associated with each course. (1100 OR 1200 OR 2200)
# 
# The link to Computer Science I offered in Fall 2021 is https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in=202109&subj_code_in=CSCI&crse_numb_in=1100
#                                                                                                                          ^^^^^^              ^^^^              ^^^^
# MORE DETAIL ON SCRAPING: 
# check the PDF 'Scraping SIS with Python' on discord


import os
import requests
import json
from bs4 import BeautifulSoup
import csv
import re

#maybe use a cache similiar to how professor used it to speed up runtime (add on to it)
#plug in semester here
baseLink = 'https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={semester}&\
subj_code_in={department}&crse_numb_in={courseNumber}'

# convert the given csv to a list
def read_csv(file_name : str = 'fall-2023.csv') -> list:
    with open(file_name, 'r', encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_reader = list(csv_reader)
        csv_reader.pop(0)
        return csv_reader

# convert the list we have to a csv file
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

# add '-' between the first 4 letters and the last 4 digits.  'CSCI 1100' -> 'CSCI-1100'
def parsePrerequisites(rawPrerequisites : str) -> str:
    if rawPrerequisites == 'None':
        return None
    retList = []
    for item in re.findall(r'\b[A-Z]{4}\s\d{4}\b', rawPrerequisites):
        retList.append(item.replace(' ','-'))
    return retList

# add '-' between the first 4 letters and the last 4 digits.  'CSCI 1100' -> 'CSCI-1100'
def parseCorequisites(rawCorequisites : str) -> str:
    if rawCorequisites == 'None':
        return None
    retList = []
    for item in re.findall(r'\b[A-Z]{4}\s\d{4}\b', rawCorequisites):
        retList.append(item.replace(' ','-'))
    return retList

def parseRaw(raw : str) -> str:
    if raw == "":
        return ""
    # May have Minimum Grade of C+/C-
    # Can't find any now, could be issue in the future
    raw = raw.replace("Undergraduate level  ","")
    raw = raw.replace("Graduate level  ","")
    raw = raw.replace("Minimum Grade of A","")
    raw = raw.replace("Minimum Grade of B","")
    raw = raw.replace("Minimum Grade of C","")
    raw = raw.replace("Minimum Grade of D","")
    return raw

def readData(filename : str) -> dict:
    with open(filename, 'r', encoding='UTF-8') as infile:
        return json.load(infile)

def saveData(filename :str, data : dict) -> None:
    with open(filename, 'w', encoding='UTF-8') as outfile:
        json.dump(data, outfile, indent=4)
    return None

def getCourseLink(semester : str, department : str, courseNumber : str) -> str:
    return baseLink.format(semester=semester, department=department, courseNumber=courseNumber)

# create a new csv
def WithoutData(filename : str, dataFilename : str, DEBUG):
    session = requests.Session()
    data = read_csv(filename)
    semester = parseSemester(filename)
    Data = dict()

    # print(data)
    for row in data:
        if (len(row) < 17): continue
        department = row[11]
        courseNumber = row[16]
        link = getCourseLink(semester, department, courseNumber)
        print(link)
        if DEBUG == 'y':
            print(link)
        page = session.get(link)
        soup = BeautifulSoup(page.content, 'html.parser', from_encoding="utf-8")
        rawbody = soup.find('td', class_='ntdefault')
        body = rawbody.text.split('\n\n')
        
        description = body[0].strip()
        description = description.split('\n \n')[0]
        description = description.replace('\n','')

        # print(description)
        prerequisites = None
        corequisites = None
        rawrequisites = ''
        for i in range(1,len(body)):
            #do print staeemtns here to help debug for new web scraper
            if body[i].strip() == 'Prerequisites:':
                rawprerequisites = parsePrerequisites(body[i+1].strip())
                rawrequisites += body[i+1].strip()
                if rawprerequisites != []:
                    prerequisites = rawprerequisites
            if body[i].strip() == 'Corequisites:':
                rawcorequisites = parseCorequisites(body[i+1].strip())
                rawrequisites += body[i+1].strip()
                if rawcorequisites != []:
                    corequisites = rawcorequisites
        row[20] = description
        row[21] = rawrequisites
        if prerequisites != None:
            row[23] = prerequisites
        if corequisites != None:
            row[24] = corequisites
        shortName = department+courseNumber
        Data[shortName] = dict()
        #add more for this to cache it faster
        Data[shortName]['description'] = description
        Data[shortName]['raw_precoreqs'] = rawrequisites
        Data[shortName]['prerequisites'] = prerequisites
        Data[shortName]['corequisites'] = corequisites
    write_csv(filename,data)
    saveData(dataFilename, Data)

# Update the existing csv
def WithData(filename : str, dataFilename : str) -> None:
    Data = readData(dataFilename)
    data = read_csv(filename)
    for row in data:
        if (len(row) < 17): continue
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
    elif season == 'summer':
        season = '05'
    elif season == 'winter':
        season = '12'
    return year+season


# course descriptions must be acquired separately because the API used in fetch_catalog_course_info.py is outdated and no longer contains course info
def getCourseDescription(semester, department, courseNumber):    
    link = getCourseLink(semester, department, courseNumber)

    webpage_response = requests.Session().get(link)
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")

    rawbody = soup.find('td', class_='ntdefault')
    body = rawbody.text.split('\n') # list of strings
    return body[1]


def main() -> None:
    filename = os.environ.get('TARGET_FILE')
    dataFilename = os.environ.get('DATA_FILE')
    hasData = os.environ.get('HAS_DATA')
    DEBUG = os.environ.get('DEBUG')

    if hasData == 'y':
        WithData(filename, dataFilename)
    else:
        semester = parseSemester(filename)
        WithoutData(filename, dataFilename, DEBUG)


if __name__ == '__main__':
    main()