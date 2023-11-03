from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import headless_login as login
import new_parse as parser
import sys
from datetime import datetime
import pytz
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from course import Course
import time
import csv_to_course


def courseUpdate(driver, term, courses):
    full_info = list()
    url = "https://sis.rpi.edu/rss/bwskfcls.p_sel_crse_search"
    driver.get(url)
    select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
    basevalue = 200000 #this number will represent the term we are looking at
    while True: #this will add the term code to the last digit, making sure that the term exists
        try:
            if ("spring" in term):
                basevalue += 1
            elif ("fall" in term):
                basevalue += 9
            elif ("summer" in term):
                basevalue += 5
            else:
                raise Exception("term not found")
        except:
            term = input("Your term may be incorrect, enter the correct term here:")
        else:
            break
    year = int(term[-2])*10 + int(term[-1]) #this is the last two digits of the year TODO: 
    basevalue += year * 100 #this makes the basevalue show our year
    select.select_by_value(str(basevalue))
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
    subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
    subjects = subject_select.options
    for i in range(len(subjects)):
        subject_select.select_by_index(i)
        driver.find_element(by = By.NAME, value = 'SUB_BTN').click()
        info = parser.getMajorCourseInfo(driver, term) # Possible TODO: just compare the parts here to make it faster (this is easier for me as I didn't write that part of the parser)
        driver.get(url)
        select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
        select.select_by_value(str(basevalue))
        driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
        subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
        [full_info.append(Course(i)) for i in info]
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
        full_info[i].addSemester(term)
        if (temp_tuple not in check_dict.keys()):
            check_dict[temp_tuple] = full_info[i]
            print("Error: course "  + check_dict[temp_tuple].name + " " + check_dict[temp_tuple].crn + " out of order, adding new course")
            continue
        new_class = full_info[i].decompose()
        old_class = check_dict[temp_tuple].decompose()
        for i in range(len(new_class)):
            if (i == 4 or i == 15):
                continue
            if (old_class[i] != new_class[i]):
                old_class[i] = new_class[i]
        check_dict[temp_tuple].list_to_class(old_class)

    courses = list()
    for i in range(len(check_dict.keys())):
        if (list(check_dict.keys())[i] in full_check):
            courses.append(check_dict[list(check_dict.keys())[i]])
        else:
            print("removed CRN: "+ list(check_dict.keys())[i][0])
    
    courses.sort()
    return courses



if __name__ == "__main__":
    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Firefox(options)
    driver.implicitly_wait(2)
    #try:
    login.login(driver)
    courses = csv_to_course.parse_csv("test_spring.csv")
    term = "spring2024"
    csv_name = 'spring2024-test.csv'
    #courses = parser.sisCourseSearch(driver, term)
    parser.writeCSV(courses, csv_name)
    time_zone = pytz.timezone('America/New_York')
    i = 0
    #try:
    while (True):
        #if (datetime.now(time_zone).strftime("%H:%M") == "00:00"):
        #    courses = parser.sisCourseSearch(driver, term)
        #    parser.writeCSV(courses, csv_name)
        #    time.sleep(40)
        courses = courseUpdate(driver, term, courses)
        parser.writeCSV(courses, csv_name)
        driver.get("http://sis.rpi.edu")
        i += 1
        print("Update # " + str(i) + " Finished")
        time.sleep(60)
    #except:
        #print("Exception occurred, exiting")
        #driver.quit()


