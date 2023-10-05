# py get-pip.py
# pip install requests
# pip install bs4
# pip install selenium


import requests
import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from bs4 import BeautifulSoup as bs
import pdb
#from lxml, based on the code from the quacs scraper and the other scraper, we will prob need to parse xml markup
# URL = "https://sis.rpi.edu"

def login(driver):
    URL = "http://sis.rpi.edu"
    
    driver.get(URL)
    driver.implicitly_wait(2)
    username_box = driver.find_element(by=By.NAME, value = "j_username")
    password_box = driver.find_element(by=By.NAME, value = "j_password")
    submit = driver.find_element(by=By.NAME, value = "_eventId_proceed")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    username_box.send_keys(username)
    password_box.send_keys(password)
    submit.click()
    while ("duosecurity" not in driver.current_url): # if you entered details incorrectly
        print("User or Password Incorrect.")
        username_box = driver.find_element(by=By.NAME, value = "j_username")
        password_box = driver.find_element(by=By.NAME, value = "j_password")
        submit = driver.find_element(by=By.NAME, value = "_eventId_proceed")
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        username_box.clear()
        username_box.send_keys(username)
        password_box.send_keys(password)
        submit.click()
    #wait = WebDriverWait(driver, timeout=10)
    #wait.until(lambda d : driver.find_elements(by = By.CLASS_NAME, value = "row display-flex align-flex-justify-content-center verification-code").getText())
    #duo_code = driver.find_element(by = By.CLASS_NAME, value = "row display-flex align-flex-justify-content-center verification-code").getText()
    print("Check for your DUO code on the browser instance and answer the prompt") #work towards making this nearly automatic
    while (driver.current_url != "https://sis.rpi.edu/rss/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu"):
        time.sleep(1)


def getCoursesInMajor(semester, subject):
    #See https://github.com/YACS-RCOS/yacs.n/blob/2023-Data-update/rpi_data/modules/postProcess.py and
    #https://github.com/overlord-bot/Overlord/blob/main/cogs/webcrawling/rpi_catalog_scraper.py
    #create soup scraper
    url = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in=202201&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj=CSCI"
    session = requests.Session()
    webres = session.get(url)
    page = webres.content
    soup = bs(page, "html.parser")
    #get all of the course codes
    table = soup.find('table', class_='datadisplaytable')
    codes = table.find_all("a")
    allCodes = []    
    for text in codes:
        #text is a long attribute tag, but we don't need all of it.
        #The text is returned as: CSCI 1100 Computer... but we only need the course code, or the 5-9th characters
        allCodes.append(text.text[5:9])
    #However this returns text if there is an a tag that isn't a course code
    #Such as CS1, which has an a tag which lists all of the sections of CS1, but only some classes have
    #this link, because why not. So we need to get rid of these strings
    for i in range(allCodes.count("re")):
        allCodes.remove("re")
    return allCodes
#Given a list of the codes, get the relevent information about each course
#This includes things such as CRN, seats and seats per section, times, location, etc
def stuff(allCodes, semester):
    for code in allCodes:
        stuff2(code, semester)
        
def stuff2(code, semester):
    #eventually we will try to generalize this, but for now I want to just get the stuff for one single page.
    url = "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse?term_in=202209&subj_in=CSCI&crse_in=2500&schd_in=L"
    session = requests.Session()
    webres = session.get(url)
    page = webres.content
    soup = bs(page, "html.parser")
    table = soup.find('table', class_='datadisplaytable')
    #There are two types of table rows in the table: titles, which hold the links to sections
    #as well as the CRNS; and defaults, which hold the credits, times, days, and locations
    rows = table.find_all("tr")
    seatcurr = seatmax = seatremain = crn = section = 0
    credits = timestart = timeend = 0
    classtype = days = location = professor = ""
    pdb.set_trace()
    for row in rows:
        if row.get("class") == "ddtitle":
            print(row.string)
            #getEnrollInfo(row, seatcurr, seatmax, seatremain, crn, section)
        elif row.has_attr("dddefault"):
            print(row.string)
            #getGenInfo(row, credits, timestart, timeend, classtype, days, location, professor)
        #:sob:
        elif row.has_attr("datadisplaytable"):
            print(row.string)
        else:
            print("Error")
    courses = []
    return courses
#We may not need allCodes, and stuff, becasue it looks like getting info from the old way will be extremely annoying
#Who knows though, but for now those methods will be commented out as we explore diff ways to scrape.
def main():
    driver = webdriver.Chrome()
    login(driver)
    #allCodes = getCoursesInMajor("202201", "CSCI")
    #stuff(allCodes, "202209")
main()
