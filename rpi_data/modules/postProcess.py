# GOAL: fix description and pre/co-requisites for courses
# Target URL: https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in=202209&subj_code_in=CSCI&crse_numb_in=2500
# SCRAPES COOURSE DESCRIPT FORM THIS FILE
# How to use:
#   DATA_FILE=summer-2023_data.json ; The cache filename
#   TARGET_FILE=summer-2023.csv     ; The file to prosses
#   HAS_DATA=y                      ; y if has the cache file, n otherwise
#   DEBUG=n                         ; y if need debug info, n otherwise

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


def read_csv(file_name : str = 'fall-2023.csv') -> list:
    with open(file_name, 'r', encoding='UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        # line_count = 0
        # for row in csv_reader2:
        #     print("row " + str(line_count) + " is: ")
        #     print(row)
        #     line_count += 1
        # print(f'Processed {line_count} lines.')

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

def WithoutData(filename : str, dataFilename : str, DEBUG):
    session = requests.Session()
    data = read_csv(filename)
    semester = parseSemester(filename)
    Data = dict()

    # print(data)
    for row in data:
        department = row[11]
        courseNumber = row[16]
        #needs department and courseNumber!!!
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


# course descriptions must be acquired separately because the API used in fetch_catalog_course_info.py is outdated and no longer contains course info
def getDescriptions():
    # print(SEMESTER)
    getCourseLink("05", "CSCI", "1000")
    year = "2023"
    season = "05"
    short_name = "CSCI"
    # link = f"http://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in={year}{season}&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj={short_name}"
    page_num = 20
    link = f"https://catalog.rpi.edu/content.php?catoid=24&navoid=606&filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bcourse_type%5D=&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D={page_num}&filter%5Bexact_match%5D=1&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&expand=1&print#acalog_template_course_filter"
    s = requests.Session()
    webpage_response = s.get(link)
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    # print(soup)

    # data2 = []
    # table = soup.find('table', attrs={'class':'table_default'})
    # rows = table.find_all('tr')
    # for row in rows:
    #     cols = row.find_all('td')
    #     print(cols)
    #     # li = cols.find("li")
    #     # for l in li:
    #     #     print(l)
        
    #     # print(cols)
    #     # cols = [ele.text.strip() for ele in cols]
    #     # data2.append([ele for ele in cols if ele]) # Get rid of empty values

    # for d in data2:
    #     print(d)


    data2 = []
    table = soup.find('table', attrs={'class':'table_default'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # for headers in cols.select('h2,h3'):
        #     print(headers)
        for ele in cols:
            if ele:
                data2.append[ele]
        data2.append([ele for ele in cols if ele]) # Get rid of empty values

    for d in data2:
        print(d)

def main() -> None:
    filename = os.environ.get('TARGET_FILE')
    dataFilename = os.environ.get('DATA_FILE')
    hasData = os.environ.get('HAS_DATA')
    DEBUG = os.environ.get('DEBUG')

    getDescriptions()
    if hasData == 'y':
        WithData(filename, dataFilename)
    else:
        semester = parseSemester(filename)
        WithoutData(filename, dataFilename, DEBUG)


if __name__ == '__main__':
    main()