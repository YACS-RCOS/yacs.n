# py get-pip.py
# pip install requests
# pip install bs4
# pip install selenium


import requests
import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup as bs
import pdb
#from lxml, based on the code from the quacs scraper and the other scraper, we will prob need to parse xml markup
# URL = "https://sis.rpi.edu"
#term format: spring2023

def login(driver):
    URL = "http://sis.rpi.edu"
    driver.get(URL)
    driver.implicitly_wait(.5)
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

def sisCourseSearch(driver, term):
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
        parseCourseTable(driver) #TODO: replace with parser for first part of csv (probably getCoursesInMajor())
        parseReqsAndDesc(driver, basevalue) #TODO: make sure this goes in the right place, probably in getCoursesInMajor
        driver.get(url)
        select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
        select.select_by_value(str(basevalue))
        driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
        subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
        
def parseCourseTable(driver):
    html = driver.page_source
    time.sleep(20)

def parseReqsAndDesc(driver, basevalue): #needs to return a list 
    url = 'https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in=' + str(basevalue) +'&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj=' #subject code needs to be appended to end before go
    subj_codes = ['ADMN','ARCH', 'ARTS'] #TODO: finish listing these... by hand...
    schools = [] #TODO: also probably do this.. by hand..
    driver.get(url)
    info = list() #[Short-Name, Full-Name, Description, raw pre/coreq text, prereq, coreq, School]
     



#We will need this later to get pre and coreqs, but for now we don't use it
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
#Given the url of a major, parse the info of that major (for now the url doesn't do anything, just use a file from sis to test)
def getMajorCourseInfo(url : str) -> list[list[str]]:
    #session = requests.Session()
    #webres = session.get(url)
    #page = webres.content
    #soup = bs(page, "html.parser")
    with open("test.html") as fp:
        soup = bs(fp, 'html.parser')
    table = soup.find('table', class_='datadisplaytable')
    rows = table.find_all("tr")
    courses = []
    for row in rows:
        #The first two rows in the page have th tags not td's, so we need to ignore them.
        data = row.find_all("td")
        if len(data) != 0:
            courses.append(processRow(data))
    return courses
#Given a row, process the data in said row including crn, course code, days, seats, etc
def processRow(data) -> list[str]:
    info = []
    #Ok so there are a bunch of cases to deal with, the big ones are the 
    for i in range(1, len(data) - 1, 1):
        if(data[i].find('a')):
            #Why is there a difference between .content and .contents
            info.append(data[i].find('a').contents)
        else:
            info.append(data[i].contents)
    
    # info[0] is crn, info[1] is major, 2 - course code, 3- section, 4 - irrelevant?, 5 - credits, 6 - class name 
    #info[7] is days, info[8] is time
    #info[9] - info[17] are cap, act, rem, etc
    #info[18] is teachers, need to format
    #info[19] are days of sem, prob need to remove, who knows
    #info[20] is location
    #Remove index[4] because it's probably useless
    info.pop(4)
    #Format profs by removing some styling that is included
    info[17] = formatTeachers(info[17])
    info = formatTimes(info)
    return info
#For now we just return the first prof that shows up, we will prob need to fix this in the future
def formatTeachers(profs : str) -> str:
    #profs is given as a navigable string so we need to convert it back to a regular one
    tmp = str(profs[0].string)
    return (tmp[:-1])
#We need to split the time into a starting and ending time, we could do it later, but it's prob easier to do it here
def formatTimes(info):
    pdb.set_trace()
    tmp = str(info[7][0])
    start = tmp[:7]
    end = tmp[:8]
    info.insert(7,start)
    info.insert(8,start)
    info.pop(9)
def main():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--remote-debugging-port=9222")
    #driver = webdriver.Chrome(options = options)
    #login(driver)
    #sisCourseSearch(driver, "fall2023")
    #url = "https://sis.rpi.edu"
    getMajorCourseInfo(" ")
    #allCodes = getCoursesInMajor("202201", "CSCI")
    
main()

