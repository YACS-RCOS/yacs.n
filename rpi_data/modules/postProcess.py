# GOAL: fix description and pre/co-requisites for courses
# Target URL: https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in=202209&subj_code_in=CSCI&crse_numb_in=2500

import requests
from bs4 import BeautifulSoup
import csv

baseLink = 'https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={semester}&subj_code_in={department}&crse_numb_in={courseNumber}'


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


if __name__ == '__main__':
    data = read_csv()
    
    write_csv(data=data)