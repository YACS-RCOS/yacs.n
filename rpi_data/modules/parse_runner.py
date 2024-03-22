#!/usr/bin/env python
import os
import sys
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import headless_login as login
import new_parse as parser
import pytz
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from course import Course
import csv_to_course
import selenium
import pdb

# COMMON PONTS OF ERROR:
#
# - If Login fails, check the headless_login file
# - If it fails in the middle of parsing that means there's some sis formatting BS going on
# (these problems are the hardest to fix because they don't make sense, check the getCourseInfo
# function and everything it calls, make sure to figure out what's going wrong)
# - If it fails in between subjects or on term selection that means they changed the website
# formatting, you'll have to check the courseUpdate function
# - remember to add a command line argument for the term that's being parsed, otherwise
# it defaults to Spring 2024 (the next term as of writing this comment) The formatting is "spring2024"

def course_update(driver, term, courses):
    schools = parser.find_all_subject_codes(driver)
    full_info = list()
    url = "https://sis.rpi.edu/rss/bwskfcls.p_sel_crse_search"
    driver.get(url)
    select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
    basevalue = parser.gen_base_value(term)
    select.select_by_value(str(basevalue))
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
    subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
    subjects = subject_select.options
    key = str(basevalue)[:4] + "-"
    for i in range(len(subjects)):
        subject_select.select_by_index(i)
        driver.find_element(by = By.NAME, value = 'SUB_BTN').click()
        info = parser.get_course_info(driver, key, schools)
        driver.get(url)
        select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
        select.select_by_value(str(basevalue))
        driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
        subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
        for i in info:
            full_info.append(i)
    full_info.sort()
    full_info.reverse()
    x = 0
    check_dict = dict()
    crn = 0
    temp_tuple = tuple()
    for i in range(len(courses)):
        crn = courses[i].crn
        stime = courses[i].stime
        temp_tuple = tuple([crn, stime])
        check_dict[temp_tuple] = courses[i]
    full_check = list()
    for i in range(len(full_info)):
        temp_tuple = tuple([full_info[i].crn, full_info[i].stime])
        full_check.append(temp_tuple)
        full_info[i].addSemester(parser.get_str_semester(full_info[i]))
        if temp_tuple not in check_dict:
            check_dict[temp_tuple] = full_info[i]
            print("Error: course "  + check_dict[temp_tuple].name + " "
                  + check_dict[temp_tuple].crn + " out of order, adding new course")
            parser.get_req_for_class(check_dict[temp_tuple])
            continue
        new_class = full_info[i].decompose()
        old_class = check_dict[temp_tuple].decompose()
        for i in range(len(new_class)):
            if i == 20:
                break
            if i in (4, 15):
                continue
            if old_class[i] != new_class[i]:
                old_class[i] = new_class[i]
        check_dict[temp_tuple].list_to_class(old_class)

    courses = list()
    for i in range(len(check_dict.keys())):
        if list(check_dict.keys())[i] in full_check:
            courses.append(check_dict[list(check_dict.keys())[i]])
        else:
            print("removed CRN: "+ list(check_dict.keys())[i][0])

    courses.sort()
    return courses



if __name__ == "__main__":
    options = Options()
    options.add_argument("--headless")
    if len(sys.argv) == 1:
        print("Error: No command argument detected. Defaulting to Spring 2024")
        term = "spring2024"
    else:
        term = sys.argv[1]
    csv_name = term + ".csv"
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    endpath = os.path.join(__location__, csv_name)
    endpath = os.path.dirname(os.path.dirname(endpath)) + "\\" + csv_name
    driver = webdriver.Firefox(options)
    driver.implicitly_wait(2)
    flag = "Failure"
    while True:
        if flag == "Failure":
            try:
                flag = login.login(driver)
            except Exception:
                flag = "Failure"
        else:
            break
    print("Login Successful")
    if not os.path.isfile(endpath):
        print("Existing csv not found, doing full parse")
        courses = parser.sis_course_search(driver, term)
        parser.write_csv(courses, endpath)
    else:
        courses = csv_to_course.parse_csv(endpath)
    time_zone = pytz.timezone('America/New_York')
    i = 0
    has_updated = False
    while True:
        if datetime.now(time_zone).strftime("%H") == "01":
            has_updated = False
        if datetime.now(time_zone).strftime("%H") == "00" and not has_updated:
            print("Doing midnight Update")
            courses = parser.sis_course_search(driver, term)
            parser.write_csv(courses, endpath)
            time.sleep(40)
            has_updated = True
        driver.get("http://sis.rpi.edu")
        courses = course_update(driver, term, courses)
        parser.write_csv(courses, endpath)
        i += 1
        print("Update # " + str(i) + " Finished")
        time.sleep(60)
