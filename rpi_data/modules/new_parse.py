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
import pandas as pd
import pdb
import copy
from course import Course
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
    course_codes_dict  = findAllSubjectCodes(driver)
    subj_codes = [info[0] for info in course_codes_dict.values()]
    schools = course_codes_dict.keys()
    driver.get(url)
    info = list() #[Short-Name, Full-Name, Description, raw pre/coreq text, prereq, coreq, School]
     
def findAllSubjectCodes(driver):
    url = 'https://catalog.rpi.edu/content.php?catoid=26&navoid=670&hl=%22subject%22&returnto=search'
    driver.get(url)
    code_school_dict = dict()
    html = driver.page_source
    soup = bs(html, 'html.parser')
    ptag = soup.find_all('p')
    look_at = []
    for all in ptag:
        if all.find('strong'):
            look_at.append(all)
    for all in look_at:
        school = ""
        for tags in all:
            if tags.name == "strong":
                school = tags.text
                school_first = school.split(' ')
                school_final = list()
                for i in school_first:
                    if '(' in i:
                        break
                    school_final.append(i)
                school = " ".join(school_final)
                code_school_dict[school] = list()
                continue
            line = tags.text.strip()
            if line is '':
                continue
            if "\xa0" in line:
                line = line.replace("\xa0", ' ')
            info = line.split(' ')
            code_school_dict[school].append([info[0], " ".join(info)])
    return code_school_dict
     

#Ok so this is very hardcoded, will prbo need to redo later on
#But for now, it takes a lab block, test block, or seminar? and fills in the missing info for it
def processSpecial(info, prevrow):
    tmp = formatTimes(info)
    tmp[18] = formatTeachers(tmp[18])
    info = prevrow
    info[6] = tmp[6]
    info[7] = tmp[7]
    info[8] = tmp[8]
    info[12] = (tmp[18])
    info[13] = (tmp[20])
    return info
#Given a string contaings the profs for a class, return a string containing only the last names of the profs
def formatTeachers(profs : str) -> str:
    index = profs.find("(P)")
    if profs == "TBA":
        #If the prof is tba we can just return
        return profs
    #Remove the (P)
    if index != -1:
        profs = profs[:index-1] + profs[index + 3:]
    #Split the last to get the last names, then reconstruct profs, can prob optimize by merging the 1st and 2nd loop
    tmp = profs.split(',')
    for i in range(0, len(tmp), 1):
        tmp[i] = tmp[i].split()[len(tmp[i].split()) -1]
    profs = ""
    for prof in tmp:
        profs += (prof + "/")
    profs = profs[:len(profs)-1]
    return profs
#We need to split the time into a starting and ending time, we could do it later, but it's prob easier to do it here
def formatTimes(info : list[str]) -> list[str]:
    #Special case where the time is tba
    if(info[7] == "TBA"):
        info.insert(8, "TBA")
        return info
    tmp = info[7]
    start = tmp[:8]
    end = tmp[9:]
    info.insert(7,start)
    info.insert(8,end)
    info.pop(9)
    return info
#Given a row, process the data in said row including crn, course code, days, seats, etc
def processRow(data, prevrow) -> list[str]:
    info = []
    for i in range(1, len(data) - 1, 1):
        #Maybe we don't need this? will need to test later
        if(data[i].find('a')):
            info.append(data[i].find('a').text)
        else:
            info.append(data[i].text)
    # info[0] is crn, info[1] is major, 2 - course code, 3- section, 4 - if class is on campus (most are), 5 - credits, 6 - class name 
    #info[7] is days, info[8] is time, info[9] - info[17] are seat cap, act, rem, waitlist, and crosslist
    #info[18] is teachers, need to format, info[19] are days of sem, info[20] is location
    #Remove index[4] because most classes are on campus, with only some grad and admin courses not being so
    #Note that this will shift the above info down by 1
    info.pop(4)
    if str(info[0]) == '\xa0':
        info = processSpecial(info, prevrow)
        return info
    #Some admin and grad courses won't have days of the week
    if (info[6] == '\xa0'):
        info[6] = "TBA"
    info[17] = formatTeachers(info[17])
    formatTimes(info)
    #Remove waitlist and crosslist stuff
    info = info[:12] + info[18:]
    #Split date into 2 :sob:
    formatDate(info)
    return info
def formatDate(info):
    splitDate = info[13].split('-')
    info.insert(13, splitDate[0])
    info.insert(14, splitDate[1])
    info.pop(15)
#Given the url of a major, parse the info for every course in that major(for now the url doesn't do anything, just use a file from sis to test)
def getMajorCourseInfo(url : str) -> list[list[str]]:
    #session = requests.Session()
    #webres = session.get(url)
    #page = webres.content
    #soup = bs(page, "html.parser")
    with open("cscitest.html") as fp:
        soup = bs(fp, 'html.parser')
    table = soup.find('table', class_='datadisplaytable')
    rows = table.find_all("tr")
    courses = []
    prevrow = []
    for row in rows:
        data = row.find_all("td")
        if len(data) != 0:
            courses.append(processRow(data, prevrow))
            prevrow = copy.deepcopy(courses[len(courses)-1])
    return courses
#Given a semester and a major, get the pre and coreqs for every class in that major
#Given a link,return the pre and co reqs for that class. Also return the major and course code to identify the class
def getReqFromLink(link, courseCode, major):
    session = requests.Session()
    webres = session.get(link)
    page = webres.content
    soup = bs(page, "html.parser")
    body = soup.find('td', class_='ntdefault')
    classInfo = body.text.strip('\n\n').split('\n\n')
    key = "Prerequisites/Corequisites"
    preKey = "Prerequisite"
    prereqs = ""
    coreqs = ""
    raw = ""
    
    desc = classInfo[0]
    #In the future replace with regex or something that isn't so hardcoded
    #If the description starts with a number, set it to nothing, basically only for weird courses
    #like 0 credit ones or topic ones or ones most people aren't taking 
    if desc.strip()[0].isdigit():
        desc = ""
    for i in range(1, len(classInfo)):
        if key in classInfo[i].strip():
            combo = classInfo[i].strip()
            combo = combo[len(key):]
            coKey = "Corequisite"
            if coKey in combo and preKey in combo:
                coreqs = combo[combo.find(coKey) + len(coKey):]
                prereqs = combo[len(preKey): combo.find(coKey)]
            elif coKey in combo:
                coreqs = combo[combo.find(coKey) + len(coKey):]
            elif preKey in combo:
                prereqs = combo[len(preKey):]
            else:
                #Default case where someone forgets the words we're looking for
                #Note that there are still more edge cases(looking at you csci 6560 and 2110)
                prereqs = combo
            prereqs = prereqs[prereqs.find(' '):].strip()
            coreqs = coreqs[coreqs.find(' '):].strip()
        if classInfo[i].strip() == (preKey + "s:"):
            raw = classInfo[i+1].strip()
    return " %!# " + prereqs + " $@^ " + coreqs + " ?^* " + raw + " %?$ " + major + '-' + courseCode + " ()! " + desc
def getReqsInMajor(semester, subject):
    #See https://github.com/YACS-RCOS/yacs.n/blob/2023-Data-update/rpi_data/modules/postProcess.py and
    #https://github.com/overlord-bot/Overlord/blob/main/cogs/webcrawling/rpi_catalog_scraper.py
    #create soup scraper
    
    url = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in=202309&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj={}".format(subject)
    session = requests.Session()
    webres = session.get(url)
    page = webres.content
    soup = bs(page, "html.parser")
    table = soup.find('table', class_='datadisplaytable')
    codes = table.find_all("a")
    allReqs = dict()
    key = "/rss/bwckctlg.p_disp_course_detail?cat_term_in="
    for link in codes:
        if key in link['href']:
            major = link.text[:4]
            code = link.text[5:9]
            link = ("https://sis.rpi.edu" + link['href'])
            codeKey = major + '-' + code
            allReqs[codeKey] = (getReqFromLink(link, code, major))
    return allReqs
#Given a semester, get the pre and co reqs for every class in that semester
#Very slow, need to speed up
def getPreCoReqs(semester):
    reqs = getReqsInMajor(semester, "CSCI")
    return reqs
#Given the info about courses (crn, seats, etc), and prereqs and desc, combine the two into one dataframe
def combineInfo(courses, reqs, school):
    print("Combining info")
    #A dictionary that stores the courses using major and code as a key, ie "CSCI-1100":[65489,CSCI,1100,01,4.000,...]
    comb = []
    ckey = "%?$"
    pkey = "%!#"
    cokey = "$@^"
    dkey = "()!"
    rkey = "?^*"
    for course in courses:
        c = Course(course)
        c.addSchool(school)
        if c.short in reqs:
            result = reqs[c.short]
            prereq = result[result.find(pkey) + len(pkey):result.find(cokey)].strip()
            coreq = result[result.find(cokey) + len(cokey):result.find(rkey)].strip()
            raw = result[result.find(rkey) + len(rkey):result.find(ckey)].strip()
            desc = result[result.find(dkey) + len(dkey):].strip()
            c.addReqs(prereq, coreq, raw, desc)
        else:
            print("error")
            sys.exit()
        comb.append(c)
    comb.sort()
    return comb
def main():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--remote-debugging-port=9222")
    #driver = webdriver.Chrome(options = options)
    #login(driver)
    #sisCourseSearch(driver, "fall2023")
    url = "https://sis.rpi.edu"
    allInfo = None
    print("Getting course info")
    courses = getMajorCourseInfo(" ")
    print("Getting co reqs")
    reqs = getPreCoReqs("202201")
    comb = combineInfo(courses, reqs)
main()

