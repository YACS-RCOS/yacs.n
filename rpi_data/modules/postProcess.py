# GOAL: fix description and pre/co-requisites for courses
# Target URL: https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in=202209&subj_code_in=CSCI&crse_numb_in=2500

import requests
from bs4 import BeautifulSoup
import csv
import re

baseLink = 'https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={semester}&\
subj_code_in={department}&crse_numb_in={courseNumber}'


def read_csv(file_name : str = 'fall-2023.csv') -> list:
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_reader = list(csv_reader)
        csv_reader.pop(0)
        return csv_reader

def write_csv(file_name : str = 'fall-2023_fixed.csv', data :list = []) -> None:
    with open(file_name, 'w') as csv_file:
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
    return re.findall(r'\b[A-Z]{4}\s[0-9]{4}\b', rawPrerequisites)


def getCourseLink(semester : str, department : str, courseNumber : str) -> str:
    return baseLink.format(semester=semester, department=department, courseNumber=courseNumber)

def main():
    session = requests.Session()
    semester = '202309'
    data = read_csv('rpi_data/modules/fall-2023.csv')

    preDescription = ''
    prePrerequisites = ''

    for row in data:
    # row = data[6]
        department = row[11]
        courseNumber = row[16]
        link = getCourseLink(semester, department, courseNumber)
        print(link)
        page = session.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        rawbody = soup.find('td', class_='ntdefault')
        body = rawbody.text.split('\n\n')
        description = body[0].strip()
        prerequisites = None
        for i in range(1,len(body)):
            if body[i].strip() == 'Prerequisites:':
                rawprerequisites = parsePrerequisites(body[i+1].strip())
                if rawprerequisites != []:
                    prerequisites = rawprerequisites
        row[20] = description
        if prerequisites != None:
            row[23] = prerequisites
    write_csv('rpi_data/modules/fall-2023_fixed.csv',data)

if __name__ == '__main__':
    main()