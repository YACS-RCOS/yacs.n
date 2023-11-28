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
#from lxml, based on the code from the quacs scraper and the other scraper, we will prob need to parse xml markup
#term format: spring2023
# TROUBLESHOOTING: remove the line "options.add_argument("--headless")" to see where the script might be stalling
# TROUBLESHOOTING: If DUO changes their website the parser will break (but in an easy to fix way, like by adding an extra button click) SIS hasn't been substantially changed since 2006 so 

def login(driver): #this is the old login function for an individual parser run, there's another login function in headless_login.py
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

def sisCourseSearch(driver, term): #main loop of the parser, goes to the course search, selects the desired term, and then loops through each subject to grab the course tables
    info = list()
    course_codes_dict = findAllSubjectCodes(driver)
    url = "https://sis.rpi.edu/rss/bwskfcls.p_sel_crse_search"
    driver.get(url)
    select = Select(driver.find_element(by=By.ID, value = "term_input_id")) # term selection dropdown
    basevalue = 200000 #this number will represent the term we are looking at
    while True: #this will add the term code to the last digit, making sure that the term exists
        try:
            # add the month value
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
    year = int(term[-2])*10 + int(term[-1]) # this is the last two digits of the year 
    basevalue += year * 100 #this makes the basevalue show our year
    select.select_by_value(str(basevalue)) # select term based on the basevalue
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click() # submit term button
    subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]')) # select subject dropdown
    subjects = subject_select.options
    subject = ""
    key = str(basevalue)[:4] + "-"
    for i in range(len(subjects)): # loops through all subjects
        start = time.time() # timer to test how long each subject takes
        subject_select.select_by_index(i) # selects a subject
        driver.find_element(by = By.NAME, value = 'SUB_BTN').click() # submits course search
        print("Getting course info")
        courses = getCourseInfo(driver, key, course_codes_dict) # creates a list of course objects
        with ThreadPoolExecutor(max_workers=50) as pool:
            pool.map(getReqForClass, courses)
        [info.append(i) for i in courses] # appends each course to our final list
        subject = info[len(info)-1].major # gets the subject we just parsed
        driver.get(url) # goes back to the start
        end = time.time()
        print("Time for " + subject +": " + str(end - start)) # prints time
        # similar to the chunk of code before the loop, gets back to the subject search
        select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
        select.select_by_value(str(basevalue))
        driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
        subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
    info.sort()
    #Because we end up sorting in reverse order, we need to reverse the list to get the correct order
    info.reverse()
    return info
#
def findAllSubjectCodes(driver) -> dict():
    url = 'https://catalog.rpi.edu/content.php?catoid=26&navoid=670&hl=%22subject%22&returnto=search' #link to a list of schools with their subject codes
    driver.get(url)
    code_school_dict = dict() # We store in a dictionary that has subject code as the key and school as the value
    html = driver.page_source
    soup = bs(html, 'html.parser')
    ptag = soup.find_all('p') # Entire text of page basically
    look_at = []
    for all in ptag: # finds all things that are important
        if all.find('strong'):
            look_at.append(all)
    for all in look_at: # in every important part
        school = ""
        for tags in all: # look at each school
            if tags.name == "strong": # if bold, it's the school name
                school = tags.text
                school_first = school.split(' ')
                school_final = list()
                for i in school_first:
                    if '(' in i:
                        break
                    school_final.append(i)
                school = " ".join(school_final)
                continue
            line = tags.text.strip() # otherwise it's a subject code
            if line == '':
                continue
            if "\xa0" in line:
                line = line.replace("\xa0", ' ')
            info = line.split(' ')
            code_school_dict[info[0]] = school # uses the current value of school for the dictionary (kind of backwards, but better for our use case)
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
#Given the starting and ending date of a class, ie 01/08-04/24, turn it into a format the backend likes - 2024-01-08, 2024-04-24
def formatDate(info : list, year : str):   
    splitDate = info[13].split('-')
    sdate = splitDate[0].split('/')
    sdate = '-'.join(sdate)
    enddate = splitDate[1].split('/')
    enddate = '-'.join(enddate)
    #Sdate and enddate are the month and days of a semester, eg 01-08 and 05-04
    info.insert(13, year + sdate)
    info.insert(14, year + enddate)
    info.pop(15)
#Turn the credits into an int, pick the greatest credit value if there is a range, eg 0.000-16.000 is returned as 16
def formatCredits(info):
    if '-' in info[4]:
        return int(float(info[4].split('-')[1]))
    return int(float(info[4]))

#Given a row in sis, process the data in said row including crn, course code, days, seats, etc
def processRow(data: list[str], prevrow: list[str], year: int) -> list[str]:
    info = []
    #Ignore the 1st element because that's the status on whether a course is open to register or not, and other parts of the app
    #Can tell that information to users
    for i in range(1, len(data) - 1, 1):
        #Edge case where the registrar decides to make a column an inconcsistent width.
        #See MGMT 2940 - Readings in MGMT in spring 2024.
        #TODO: Accomodate for colspans different than 2. 
        #See https://stackoverflow.com/questions/13263373/beautifulsoup-parsing-tag-table-html-especially-colspan-and-rowspan to start
        if(data[i].has_attr("colspan")):
            info.append("TBA")
            info.append("TBA")  
        else:
            info.append(data[i].text)
    if len(info) != 21:
        print("error in: ")
        print(info[0])
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
    formatDate(info, year)
    info[12] = formatTeachers(info[12])
    #Some classes have a credit value ranging from 0-12, just pick the biggest credit value
    #We do this instead of keeping the range because the backend does not like having a string for the credit value.
    info[4] = formatCredits(info)
    return info
#Given a course, return the semester followed by the year, eg if the start date of a course is 2024-01-08, then this will return SPRING 2024
def getStrSemester(c : Course) -> str:
    val = str(getSemester(c))
    date = val[:4]
    if val[4:] == "01":
        date = "SPRING " + date
    elif val[4:] == "09":
        date = "FALL " + date
    elif val[4:] == "05":
        date = "SUMMER " + date
    elif val[4:] == "12":
        date = "WINTER " + date
    return date
#Given a school year and a dictionary of every major to names of their schools, parse all of the info for every course in a major.
def getCourseInfo(driver, year:str, schools : dict) -> list:
    html = driver.page_source
    soup = bs(html, 'html.parser')
    table = soup.find('table', class_='datadisplaytable')
    rows = table.find_all("tr")
    courses = []
    prevrow = []
    for row in rows:
        data = row.find_all("td")
        if len(data) != 0:
            tmpCourse = (processRow(data, prevrow, year))
            prevrow = copy.deepcopy(tmpCourse)
            c = Course(tmpCourse)
            c.addSemester(getStrSemester(c))
            if c.major in schools:
                c.addSchool(schools[c.major])
            else:
                #A catch all for courses that aren't listed on the offical catalog, such as ADMN or BSUN courses. 
                #If in the future there are too many of these were it shouldn't be, then we will have to find a better solution
                c.addSchool("Interdisciplinary and Other")
            courses.append(c)
    return courses
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
    #If the description starts with a number, set it to nothing.
    #Only happens is the course does not have a description and skips into credit value or something else.
    #
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
    return retList
#Add the prereqs for a course
def getReqForClass(course: Course) -> None:
    semester = getSemester(course)
    url = "https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={}&subj_code_in={}&crse_numb_in={}".format(semester, course.major, course.code)
    session = requests.session()
    webres = session.get(url)
    course.addReqsFromList(getReqFromLink(webres, course.code, course.major))
#Given a course, get the integer representation of that course's semester
def getSemester(course: Course):
    dates = course.sdate.split("-")
    month = dates[1]
    year = dates[0]
    sem = year
    if month == "08" or month == "09":
        sem += "09"
    else:
        sem += month
    return sem
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

#main()

