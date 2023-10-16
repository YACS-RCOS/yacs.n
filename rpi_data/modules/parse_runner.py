from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import headless_login as login
import new_parse as parser
import sys
from datetime import datetime
import pytz
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time

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
        info = parser.getMajorCourseInfo(driver) # Possible TODO: just compare the parts here to make it faster (this is easier for me as I didn't write that part of the parser)
        driver.get(url)
        select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
        select.select_by_value(str(basevalue))
        driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
        subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
        full_info.append(i for _ in info)
    for i in range(len(full_info)):
        if (courses[i].crn != full_info[i][0]):
            print("Error: course"  + courses.crn + "out of order")
            continue
        if (courses[i].max != full_info[i][9]):
            courses[i].max = full_info[i][9]
        if (courses[i].curr != full_info[i][10]):
            courses[i].curr = full_info[i][10]
        if (courses[i].rem != full_info[i][11]):
            courses[i].rem = full_info[i][11]


if __name__ == "__main__":
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options)
    login.login(driver)
    term = sys.argv[1]
    csv_name = sys.argv[2]
    courses = parser.sisCourseSearch(driver, term)
    parser.writeCSV(courses, csv_name)
    time_zone = pytz.timezone('America/New_York')
    while (True):
        if (datetime.now(time_zone).strftime("%H:%M") == "00:00"):
            courses = parser.sisCourseSearch(driver, term)
            parser.writeCSV(courses, csv_name)
            time.sleep(40)
        courses = courseUpdate(driver, term, courses)
        parser.writeCSV(courses, csv_name)
        time.sleep(20)


