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
from concurrent.futures import ThreadPoolExecutor
import sys
import datetime
#from lxml, based on the code from the quacs scraper and the other scraper, we will prob need to parse xml markup
# URL = "https://sis.rpi.edu"
#term format: spring2023

def login(driver):
    URL = "http://sis.rpi.edu"
    driver.get(URL) # uses a selenium webdriver to go to the sis website, which then redirects to the rcs auth website
    driver.implicitly_wait(.5)
    username_box = driver.find_element(by=By.NAME, value = "j_username") # creates a variable which contains an element type, so that we can interact with it, j_username is the username text box
    password_box = driver.find_element(by=By.NAME, value = "j_password") # j_password is the password box
    submit = driver.find_element(by=By.NAME, value = "_eventId_proceed") # _eventId_proceed is the submit button
    username = input("Enter Username: ") # take user input of user and password
    password = input("Enter Password: ")
    username_box.send_keys(username) # enters the username
    password_box.send_keys(password) # enters the password
    submit.click() # click the submit button
    while ("duosecurity" not in driver.current_url): # if you entered details incorrectly, the loop will be entered as you aren't on the duo verfication website (redo what we did before)
        print("User or Password Incorrect.")
        username_box = driver.find_element(by=By.NAME, value = "j_username") # we have to redefine the variables because the webpage reloads
        password_box = driver.find_element(by=By.NAME, value = "j_password")
        submit = driver.find_element(by=By.NAME, value = "_eventId_proceed")
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        username_box.clear() # the username box by default has your previous username entered, so we clear it
        username_box.send_keys(username)
        password_box.send_keys(password)
        submit.click()
    print("Check for your DUO code on the browser instance and answer the prompt (Remember to trust/not trust the device)") #work towards making this nearly automatic
    while (driver.current_url != "https://sis.rpi.edu/rss/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu"): #check that the user has inputted their duo code and that it redirected to the sis main page
        time.sleep(1)

def sisCourseSearch(driver, term):
    info = list()
    course_codes_dict = findAllSubjectCodes(driver)
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
    subject = ""
    for i in range(len(subjects)):
        start = time.time()
        subject_select.select_by_index(i)
        driver.find_element(by = By.NAME, value = 'SUB_BTN').click()
        print("Getting course info")
        courses = getMajorCourseInfo(driver)
        subject = courses[0][1]
        if (subject not in course_codes_dict.keys()):
            school = "Interdisciplinary and Other"
        else:
            school = course_codes_dict[subject]
        print("Getting co reqs: " + subject)
        reqs = getReqsInMajor(str(basevalue), subject)
        comb = combineInfo(courses, reqs, school, term)
        driver.get(url)
        end = time.time()
        print("Time for " + subject +": " + str(end - start))
        select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
        select.select_by_value(str(basevalue))
        driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
        subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
        [info.append(i) for i in comb]
    info.sort()
    #Because we end up sorting in reverse order, we need to reverse the list to get the correct order
    info.reverse()
    return info
        
def parseCourseTable(driver):
    html = driver.page_source
    time.sleep(20)

def parseReqsAndDesc(driver, basevalue):
    url = 'https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in=' + str(basevalue) +'&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj=' #subject code needs to be appended to end before go
    course_codes_dict  = findAllSubjectCodes(driver)
    subj_codes = [info[0] for info in course_codes_dict.values()]
    schools = course_codes_dict.keys()
    driver.get(url)
    info = list()
     
def findAllSubjectCodes(driver):
    url = 'https://catalog.rpi.edu/content.php?catoid=26&navoid=670&hl=%22subject%22&returnto=search' #link to a list of schools with their subject codes
    driver.get(url)
    code_school_dict = dict() # We store in a dictionary of schools ask keys with lists of subject codes and full subject names as values
    html = driver.page_source
    soup = bs(html, 'html.parser')
    ptag = soup.find_all('p') # Entire text of page basically
    look_at = []
    for all in ptag: # finds all things that are important
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
                continue
            line = tags.text.strip()
            if line == '':
                continue
            if "\xa0" in line:
                line = line.replace("\xa0", ' ')
            info = line.split(' ')
            code_school_dict[info[0]] = school
    return code_school_dict
     

#But for now, it takes a lab block, test block, or seminar? and fills in the missing info for it
def processSpecial(info, prevrow) -> list[str]:
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
    #Split the profs into diff arrays, then get the last name and return that
    tmp = profs.split(',')
    profs = ""
    for i in range(0, len(tmp), 1):
        tmp[i] = tmp[i].split()[len(tmp[i].split()) -1]
        profs += tmp[i] + "/"
    profs = profs[:len(profs)-1]
    return profs
#We need to split the time into a starting and ending time, we could do it later, but it's prob easier to do it here
def formatTimes(info : list[str]) -> list[str]:
    #Special case where the time is tba
    if(info[7] == "TBA"):
        info.insert(8, "")
        info[7] = ""
        return info
    #Split the time in two, and then insert the split times as the start and end time
    splitTime = info[7].split('-')
    start = splitTime[0]
    end = splitTime[1]
    info.insert(7,start)
    info.insert(8,end)
    #Pop to remove original time
    info.pop(9)
    return info
#splitTime = info[7].split('-')
    #stime = datetime.datetime.strptime(splitTime[0], '%I:%M %p')
    #etime = datetime.datetime.strptime(splitTime[1], '%I:%M %p')
    #info.insert(7,stime.date())
    #info.insert(8,etime.date())
#Given a row, process the data in said row including crn, course code, days, seats, etc
def processRow(data, prevrow) -> list[str]:
    info = []
    for i in range(1, len(data) - 1, 1):
        #Maybe we don't need this? will need to test later
        if(data[i].has_attr("colspan")):
            info.append("TBA") # The time seems to be none, TBA is a good placeholder for now
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
        info[6] = ""
    info[17] = formatTeachers(info[17])
    formatTimes(info)
    #Remove waitlist and crosslist stuff
    info = info[:12] + info[18:]
    #Split the date into start and end date
    formatDate(info)
    #Some classes have a credit value ranging from 0-12    
    info[4] = formatCredits(info)
    return info
def formatDate(info):
    key = "2023-"
    splitDate = info[13].split('-')
    sdate = splitDate[0].split('/')
    sdate = '-'.join(sdate)
    enddate = splitDate[1].split('/')
    enddate = '-'.join(enddate)
    info.insert(13, key + sdate)
    info.insert(14, key + enddate)
    info.pop(15)
def formatCredits(info):
    if '-' in info[4]:
        return int(float(info[4].split('-')[1]))
    return int(float(info[4]))
#Given the url of a major, parse the info for every course in that major
def getMajorCourseInfo(driver) -> list[list[str]]:
    html = driver.page_source
    soup = bs(html, 'html.parser')
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
def getReqFromLink(webres, courseCode, major):
    page = webres.content
    soup = bs(page, "html.parser")
    body = soup.find('td', class_='ntdefault')
    classInfo = body.text.strip('\n\n').split('\n\n')
    for i in range(0,len(classInfo),1):
        while '\n' in classInfo[i]:
            classInfo[i] = classInfo[i].replace('\n','')
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
    
    url = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in={}&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj={}".format(semester, subject)
    session = requests.Session()
    webres = session.get(url)
    page = webres.content
    soup = bs(page, "html.parser")
    
    table = soup.find('table', class_='datadisplaytable')
    codes = table.find_all("a")
    allReqs = dict()
    key = "/rss/bwckctlg.p_disp_course_detail?cat_term_in=" + semester
    url_list = list()
    for link in codes:
        if key in link['href']:
            link = ("https://sis.rpi.edu" + link['href'])
            url_list.append(link)
    sessions = list()
    start = time.time()
    with ThreadPoolExecutor(max_workers=50) as pool:
        sessions = list(pool.map(get_url, url_list))
    end = time.time()
    print(str(end - start))
    i = 0
    for session in sessions:
        link = url_list[i]
        major = link[link.find("subj_code_in=") + len("subj_code_in="):link.find("subj_code_in=") + len("subj_code_in=") + 4]
        code = link[link.find("crse_numb_in=") + len("crse_numb_in="):]
        codeKey = major + '-' + code
        allReqs[codeKey] = (getReqFromLink(session, code, major))
        i += 1
    return allReqs
#Given a semester, get the pre and co reqs for every class in that semester
#Very slow, need to speed up
#Given the info about courses (crn, seats, etc), and prereqs and desc, combine the two into one dataframe
def combineInfo(courses:list, reqs:dict, school:str, semester:str):
    print("Combining info")
    comb = []
    ckey = "%?$"
    pkey = "%!#"
    cokey = "$@^"
    dkey = "()!"
    rkey = "?^*"
    sem = semester
    index = 0
    #This maybe works? idk
    for letter in sem:
        if not letter.isdigit():
            letter = letter.upper()
            index += 1
    sem = sem[:index] + " " + sem[index:]
    for course in courses:
        c = Course(course)
        c.addSchool(school)
        c.addSemester(sem)
        if c.short in reqs:
            result = reqs[c.short]
            prereq = result[result.find(pkey) + len(pkey):result.find(cokey)].strip()
            coreq = result[result.find(cokey) + len(cokey):result.find(rkey)].strip()
            raw = result[result.find(rkey) + len(rkey):result.find(ckey)].strip()
            tmpPre = []
            tmpCo = []
            if len(prereq) > 3:
                tmpPre = prereq.split("and")
            if len(coreq) > 3:
                tmpCo = coreq.split("and")
            desc = result[result.find(dkey) + len(dkey):].strip()
            c.addReqs(tmpPre, tmpCo, raw, desc)
        else:
            print("error")
        comb.append(c)
    return comb
#Given a list of courses, write the courses to a csv
def writeCSV(info:list, filename: str):
    #Ok we're missing course type, offer frequency
    #Idk what to do about those yet
    columnNames = ['course_name', 'course_type', 'course_credit_hours', 
        'course_days_of_the_week', 'course_start_time', 'course_end_time', 
        'course_instructor', 'course_location', 'course_max_enroll', 'course_enrolled', 
        'course_remained', 'course_department', 'course_start_date', 'course_end_date', 
        'semester', 'course_crn', 'course_level', 'course_section', 'short_name', 'full_name', 
        'description', 'raw_precoreqs','offer_frequency', 'prerequisites', 'corequisites', 
        'school']
    decomposed = [[]] * len(info)
    for i in range(0, len(info), 1):
        decomposed[i] = info[i].decompose()
    df = pd.DataFrame(decomposed, columns = columnNames)
    df.to_csv(filename, index=False)
    

def get_url(url):
    session = requests.Session()
    return session.get(url)

def main():
    options = Options()
    #options.add_argument("--no-sandbox")
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--headless")
    #options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Firefox()
    login(driver)
    start = time.time()
    final = sisCourseSearch(driver, "fall2023")
    end = time.time()
    writeCSV(final, "test.csv")
    print("Total Elapsed: " + str(end - start))
   
main()

