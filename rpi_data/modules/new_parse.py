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
import cProfile
#from lxml, based on the code from the quacs scraper and the other scraper, we will prob need to parse xml markup
# URL = "https://sis.rpi.edu"
#term format: spring2023

def login(driver):
    URL = "http://sis.rpi.edu"
    driver.get(URL) # uses a selenium webdriver to go to the sis website, which then redirects to the rcs auth website
    driver.implicitly_wait(4)
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
    key = str(basevalue)[:4] + "-"
    for i in range(len(subjects)):
        start = time.time()
        subject_select.select_by_index(i)
        driver.find_element(by = By.NAME, value = 'SUB_BTN').click()
        print("Getting course info")
        courses = update(driver, key, basevalue)
        #subject = courses[0][1]
        [info.append(i) for i in courses]
        subject = info[len(info)-1].major
        # if (subject not in course_codes_dict.keys()):
        #     school = "Interdisciplinary and Other"
        # else:
        #     school = course_codes_dict[subject]
        # print("Getting co reqs: " + subject)
        # reqs = getReqsInMajor(str(basevalue), subject)
        # comb = combineInfo(courses, reqs, school, term)
        driver.get(url)
        end = time.time()
        print("Time for " + subject +": " + str(end - start))
        select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
        select.select_by_value(str(basevalue))
        driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
        subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
        # [info.append(i) for i in comb]
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
     

#For cases where courses are missing a significant amount of information. Exclusevly (need to test this though to see if anything slips through)
#used for test blocks, recitations, and labs
def processSpecial(info, prevrow) -> list[str]:
    tmp = formatTimes(info)
    tmp[18] = formatTeachers(tmp[18])
    info = prevrow
    info[6] = tmp[6]
    info[7] = tmp[7]
    info[8] = tmp[8]
    info[12] = tmp[18]
    info[15] = tmp[20]
    return info
#Given a string contaings the profs for a class, return a string containing only the last names of the profs seperated by a slash.
def formatTeachers(profs : str) -> str:
    if profs == "TBA":
        return profs
    index = profs.find("(P)")
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
#Format the times of the classes into a start and ending time. ie 2:00pm-3:50pm becomes 2:00pm as the start time and 3:50pm as the end time 
def formatTimes(info : list[str]) -> list[str]:
    #Special case where the time is tba or there isn't a valid time see admin 1030 or admin 1100 in spring 2024
    if(info[7] == "TBA" or ':' not in info[7]):
        info.insert(8, "")
        info[7] = ""
        return info
    #Remove any spaces that are in the time. Spaces in the time may cause a csv issue.
    if info[7] != "":
        while " " in info[7]:
            info[7] = info[7].replace(" ", "")
    splitTime = info[7].split('-')
    start = splitTime[0]
    end = splitTime[1]
    info.insert(7,start)
    info.insert(8,end)
    #Pop to remove original time
    info.pop(9)
    return info
#Given a row in sis, process the data in said row including crn, course code, days, seats, etc
def processRow(data, prevrow, key) -> list[str]:
    info = []
    #Ignore the 1st element because that's the status on whether a course is open to register or not, and other parts of the app
    #Can tell that information to users
    for i in range(1, len(data) - 1, 1):
        #Edge case where the registrar decides to make a column an inconcsistent width.
        #See MGMT 2940 - Readings in MGMT in spring 2024.
        if(data[i].has_attr("colspan")):
            info.append("TBA") # The time seems to be none, TBA is a good placeholder for now
            info.append("TBA")  
        else:
            info.append(data[i].text)
    # info[0] is crn, info[1] is major, 2 - course code, 3- section, 4 - if class is on campus (most are), 5 - credits, 6 - class name 
    #info[7] is days, info[8] is time, info[9] - info[17] are seat cap, act, rem, waitlist, and crosslist
    #info[18] are the profs, info[19] are days of the sem that the course spans, and info[20] is location
    #Remove index[4] because most classes are on campus, with exceptions for some grad and doctoral courses.    
    info.pop(4)
    
    #Note that this will shift the above info down by 1 to
    # info[0] crn, info[1]  major, 2 - course code, 3- section, 4 - credits, 5 - class name 
    #info[6] is days, info[7] time, info[8] - info[16] seat cap, act, rem, waitlist, and crosslist
    #info[17] profs, info[18] days of sem, and info[19] location
    #The above info is what we are working with for the rest of the method

    #If the crn is empty, then the course is most likely a lab, test, or recitation, so process this row seperately.
    if str(info[0]) == '\xa0':
        info = processSpecial(info, prevrow)
        return info
    #Some admin and grad courses won't have days of the week
    #Also the backend doesn't like the days of the week being TBA
    if (info[6] == '\xa0' or info[6] == "TBA"):
        info[6] = ""
    #Generally speaking methods that affect info should come in the order that the affect elements, ie 
    #time formatitng should come before prof or date formatting because time is at info[6] while date and
    #prof is after. Not doing this can lead to the scraper crashing on some edge cases (see admin 1030 in spring 2024)
    formatTimes(info)
    #Remove waitlist and crosslist stuff
    info = info[:12] + info[18:]
    #Split the date into start and end date
    formatDate(info, key)
    info[12] = formatTeachers(info[12])
    #Some classes have a credit value ranging from 0-12, just pick the biggest credit value
    #We do this instead of keeping the range because the backend does not like having a string for the credit value.
    info[4] = formatCredits(info)
    return info
#Given the starting and ending date of a class, ie 01/08-04/24, turn it into a format the backend likes - 2024-01-08, 2024-04-24
def formatDate(info : list, key : str):   
    splitDate = info[13].split('-')
    sdate = splitDate[0].split('/')
    sdate = '-'.join(sdate)
    enddate = splitDate[1].split('/')
    enddate = '-'.join(enddate)
    
    info.insert(13, key + sdate)
    info.insert(14, key + enddate)
    info.pop(15)
#Turn the credits into an int, pick the greatest credit value if there is a range, eg 0.000-16.000 is returned as 16
def formatCredits(info):
    if '-' in info[4]:
        return int(float(info[4].split('-')[1]))
    return int(float(info[4]))
#Given the url from sis of a major, parse the course info (crn, time, date, profs, etc) and store it in a list.
def getMajorCourseInfo(driver, key) -> list[list[str]]:
    html = driver.page_source
    soup = bs(html, 'html.parser')
    table = soup.find('table', class_='datadisplaytable')
    rows = table.find_all("tr")
    courses = []
    prevrow = []
    for row in rows:
        data = row.find_all("td")
        if len(data) != 0:
            courses.append(processRow(data, prevrow, key))
            #Keep a copy of the previous course in order to update info for lab blocks, test blocks, etc, easily.
            prevrow = copy.deepcopy(courses[len(courses)-1])
    return courses
#Generate a new csv that will update the old one?
def update(driver, key:str, baseval:int):
    html = driver.page_source
    soup = bs(html, 'html.parser')
    table = soup.find('table', class_='datadisplaytable')
    rows = table.find_all("tr")
    courses = []
    prevrow = []
    for row in rows:
        data = row.find_all("td")
        if len(data) != 0:
            tmpCourse = (processRow(data, prevrow, key))
            prevrow = copy.deepcopy(tmpCourse)
            c = Course(tmpCourse)
            c.addReqsFromList(getReqForClass(baseval, c.major, c.code))
            courses.append(c)
    return courses
    writeCSV(courses, "test.csv")
#Given a url for a course, as well as the course code and major, return a list of prereqs, coreqs, and raw
def getReqFromLink(webres, courseCode, major) -> list:
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
    #If the description starts with a number, set it to nothing.
    #Only happens is the course does not have a description and skips into credit value or something else.
    #We don't display those courses anyways.
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
            prereqs = prereqs[prereqs.find(' '):255].strip()
            coreqs = coreqs[coreqs.find(' '):255].strip()
        if classInfo[i].strip() == (preKey + "s:"):
            raw = classInfo[i+1].strip()
    retList = [prereqs, coreqs, raw, desc]
    #pdb.set_trace()
    #return " %!# " + prereqs + " $@^ " + coreqs + " ?^* " + raw + " %?$ " + major + '-' + courseCode + " ()! " + desc
    return retList
#Given a semester and major, get all of the prereqs and coreqs for every class in that major that are being offered that semester.
#Note that most of the slowdown in the program occurs here. Best that I can tell, this cannot be significantly optimized as 
#the website is just slow to load, and we can't really fix that. Though i'm sure there's some optimizations you can make if you really want to
def getReqsInMajor(semester : int, subject : str):
    #See https://github.com/YACS-RCOS/yacs.n/blob/2023-Data-update/rpi_data/modules/postProcess.py and
    #https://github.com/overlord-bot/Overlord/blob/main/cogs/webcrawling/rpi_catalog_scraper.py    
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
#Given a course sem, a subject, and a course code, get the prereqs, coreqs, and desc for a class.
def getReqForClass(semester : int, subject : str, code : int) -> list:
    url = "https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={}&subj_code_in={}&crse_numb_in={}".format(semester, subject, code)
    session = requests.session()
    webres = session.get(url)
    page = webres.content
    soup = bs(page, "html.parser")
    #pdb.set_trace()
    return getReqFromLink(webres, code, subject)

#Given a list of courses from sis or the prereq webpage, combine the two so that every course has a list of prereqs associated with it
def combineInfo(courses:list, reqs:dict, school:str, semester:str) -> list:
    print("Combining info")
    comb = []
    sem = semester
    index = 0
    #COnvert the semester into an uppercase semester to make the database happy.
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
            prereq = result[0].strip()
            coreq = result[1].strip()
            raw = result[2].strip()
            tmpPre = []
            tmpCo = []
            if len(prereq) > 3:
                tmpPre = prereq.split("and")
            if len(coreq) > 3:
                tmpCo = coreq.split("and")
            desc = result[4].strip()
            c.addReqs(tmpPre, tmpCo, raw, desc)
        else:
            print("error")
        comb.append(c)
    return comb
#Given a list of courses, write the courses to a csv specified in the filename
def writeCSV(info:list, filename: str):
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
    
#What does this do?
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
    final = sisCourseSearch(driver, "spring2024")
    end = time.time()
    writeCSV(final, "test.csv")
    print("Total Elapsed: " + str(end - start))
   
cProfile.run('main()')

