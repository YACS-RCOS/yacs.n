#!/usr/bin/env python
import requests
import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import pdb
import copy
from course import Course
from concurrent.futures import ThreadPoolExecutor
import sys
import headless_login as login
# from lxml, based on the code from the quacs scraper and the other scraper, we will prob need to parse xml markup
# term format: spring2023, fall2023, summer2023, hartford2023, enrichment2023
# TROUBLESHOOTING: remove the line "options.add_argument("--headless")" to see where the script might be stalling
# TROUBLESHOOTING: If DUO changes their website the parser will break (but in an easy to fix way, like by adding an extra button click) SIS hasn't been substantially changed since 2006 so it probably won't be changed any time soon.
# The sisCourseSearch function serves a similar purpose as the courseUpdate function, so if you make any changes to the the top half of either (before the for loop), try to do it for both

def genBasevalue(term): #this function returns the code sis uses for a specific term
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
            elif ("hartford" in term):
                basevalue += 10
            elif ("enrichment" in term):
                basevalue += 12
            else:
                raise Exception("term not found")
        except Exception:
            term = input("Your term may be incorrect, enter the correct term here:")
        else:
            break
    year = int(term[-2])*10 + int(term[-1]) # this is the last two digits of the year 
    basevalue += year * 100 #this makes the basevalue show our year
    return basevalue

def sisCourseSearch(driver, term, course_codes_dict): #main loop of the parser, goes to the course search, selects the desired term, and then loops through each subject to grab the course tables
    info = list()
    
    url = "https://sis.rpi.edu/rss/bwskfcls.p_sel_crse_search"
    driver.get(url)
    select = Select(driver.find_element(by=By.ID, value = "term_input_id")) # term selection dropdown
    basevalue = genBasevalue(term)
    try:
        select.select_by_value(str(basevalue)) # select term based on the basevalue
    except Exception:
        print("The term you entered does not exist.")
        sys.exit()
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
            pool.map(getReqForClass, courses, course_codes_dict.keys())
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

def findAllSubjectCodes(driver) -> dict[str, str]:
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
     

#For courses that do not have a crn. 99% of the time, these will be lab blocks, test blocks, or recitations
def processSpecial(info, prevrow) -> list[str]:
    #If this is ever called on an incorrect course.
    #Shouldn't happen but who knows 
    if prevrow == None:
        print("course has no crn but first in major")
        return info #Maybe just exit the program instead?
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
    start = splitTime[0].upper()
    end = splitTime[1].upper()
    if (start[0] == '0'):
        start = start[1:]
    if (end[0] == '0'):
        end = end[1:]
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
#Note that we remove a lot of info from the row in SIS, this is to match the format that the csv is expecting
#See Fall 2023 or any other csv in the repository.
def processRow(data: list[str], prevrow: list[str], year: int) -> list[str]:
    info = []
    #The first and last elements of the row are useful to us as other parts of the application handle those
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
        print("Length error in: ")
        print(info[0])
    # info[0] is crn, info[1] is major, 2 - course code, 3- section, 4 - if class is on campus (most are), 5 - credits, 6 - class name 
    #info[7] is days, info[8] is time, info[9] is total course capactiy, info[10] is number of students enrolled,
    #info[11] is the number of seats left, info[12] - waitlist capacity, info[13] - waitlist enrolled, info[14] - waitlist spots left,
    #info[15] - crosslist capacity, info[16] - crosslist enrolled, info[17] - crosslist seats left,
    #info[18] are the profs, info[19] are days of the sem that the course spans, and info[20] is location
    #Remove index[4] because most classes are on campus, with exceptions for some grad and doctoral courses.    
    info.pop(4)
    
    #Note that this will shift the above info down by 1 to
    # info[0] crn, info[1]  major, 2 - course code, 3- section, 4 - credits, 5 - class name 
    #info[6] is days, info[7] time, info[8] - info[16] actual, waitlist, and crosslist capacity, enrolled, remaining
    #info[17] profs, info[18] days of sem, and info[19] location
    #The above info is what we are working with for the rest of the method

    #If the crn is empty, then the course is most likely a lab, test, or recitation, so process this row seperately.
    if str(info[0]) == '\xa0':
        info = processSpecial(info, prevrow)
        return info
    #Some admin and grad courses won't have days of the week
    #Also the backend doesn't like the days of the week being TBA
    info[6] = info[6].strip('\xa0')
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
    elif val[4:] == "10":
        date = "HARTFORD " + date
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
# takes a raw phrase and returns a list of all of the course codes included, with repeats
def findCourseCodes(raw, subject_codes) -> list:
    course_codes = []
    for i in subject_codes:
        while (i in raw):
            find = raw.find(i)
            text = raw[find:find + 9]
            raw = raw[:find] + raw[find + 9:]
            if (text[4] != " " or not text[5].isdigit()):
                continue
            course_codes.append(text)
    return course_codes
#Given a url for a course, as well as the course code and major, return a list of prereqs, coreqs, and description of the course
#Eg. ITWS 2110 - https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in=202401&subj_code_in=ITWS&crse_numb_in=2110 
# Prereqs - ITWS 1100
# Coreqs - CSCI 1200
# Raw -  Undergraduate level CSCI 1200 Minimum Grade of D and Undergraduate level ITWS 1100 Minimum Grade of D or Prerequisite Override 100 
# Description - This course involves a study of the methods used to extract and deliver dynamic information on the World Wide Web.
# The course uses a hands-on approach in which students actively develop Web-based software systems.
# Additional topics include installation, configuration, and management of Web servers.
# Students are required to have access to a PC on which they can install software such as a Web server and various programming environments.

def getReqFromLink(webres, subject_codes) -> list:
    page = webres.content
    soup = bs(page, "html.parser")
    body = soup.find('td', class_='ntdefault')
    #The page is full of \n\n's for some reason, and this nicely splits it into sections
    classInfo = body.text.strip('\n\n').split('\n\n')
    for i in range(0,len(classInfo),1):
        while '\n' in classInfo[i]:
            #Some \n's can make it into the parsed data, so we need to get rid of them.
            classInfo[i] = classInfo[i].replace('\n','')
    key = "Prerequisites/Corequisites: "
    preKey = "Prerequisite"
    coKey = "Corequisite"
    extraKey = "Co-listed"
    creditKey = "Credit Hours"
    prereqs = []
    coreqs = []
    raw = ""
    desc = classInfo[0]
    # uses full so that we can just get all info
    full = "".join(classInfo).strip()
    # look for starting key
    if (key in full):
        raw = full.split(key)[1].split(creditKey)[0]
    else: 
        raw = full
    if (key not in raw and coKey not in raw and preKey not in raw):
        return [str([]), str([]), "", desc]
    #If the course does not have a description, usually this menas that classInfo[0] will be the credit value.
    if desc.strip()[0].isdigit():
        desc = ""
    #removes Prereq/Coreq starting keyphrase so we can focus on just coreqs, just prereqs, or both if it isn't distinguished
    raw = raw.replace(key, "")
    raw_prereqs = ""
    raw_coreqs = ""
    # checks if courses are prereqs, coreqs or both
    if (preKey in raw and coKey in raw):
        if (raw.find(coKey) < raw.find(preKey)):
            raw_coreqs = raw.split(coKey)[1].split(preKey)[0]
            raw_prereqs = raw.split(preKey)[1]
        else:
            raw_prereqs = raw.split(preKey)[1].split(coKey)[0]
            raw_coreqs = raw.split(coKey)[1]
    elif (preKey in raw):
        raw_prereqs = raw
    elif (coKey in raw):
        raw_coreqs = raw
    else:
        raw_prereqs = raw
        raw_coreqs = raw
    #checks for co-listed courses to not include
    if (extraKey in raw_prereqs):
        raw_prereqs = raw_prereqs.split(extraKey)[0]
    
    if (extraKey in raw_coreqs):
        raw_prereqs = raw_coreqs.split(extraKey)[0]
    # look for course codes
    prereqs = findCourseCodes(raw_prereqs, subject_codes)
    coreqs = findCourseCodes(raw_coreqs, subject_codes)
    # take out repeats
    prereqs = list(set(prereqs))
    coreqs = list(set(coreqs))
    # makes raw both prereqs and coreqs if they are different
    if (raw_prereqs != raw_coreqs):
        raw = raw_prereqs + " " + raw_coreqs
    else:
        if (extraKey in raw):    
            raw = raw.split(extraKey)
    retList = [str(prereqs), str(coreqs), raw, desc]
    return retList
#Add the prereqs for a course to that course
def getReqForClass(course: Course, course_codes: list) -> None:
    semester = getSemester(course)
    url = "https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={}&subj_code_in={}&crse_numb_in={}".format(semester, course.major, course.code)
    session = requests.session()
    webres = session.get(url)
    course.addReqsFromList(getReqFromLink(webres, course_codes))
#Given a course, return the basevalue of that course, eg 2024-01 is returned as 202401
def getSemester(course: Course) -> int:
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

# This main function is helpful for running the full parser standalone, without needing environmental variables.

if __name__ == "__main__":
    options = Options()
    fp = webdriver.FirefoxProfile()
    # fp.set_preference("network.cookie.cookieBehavior", 2)
    fp.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0",
    )
    options.profile = fp
    driver = webdriver.Firefox(options)
    driver.delete_all_cookies()
    try:
        driver.implicitly_wait(2)
        course_codes_dict = findAllSubjectCodes(driver)
        login.login(driver)
        start = time.time()
        final = sisCourseSearch(driver, "spring2024", course_codes_dict)
        end = time.time()
        writeCSV(final, "test.csv")
        print("Total Elapsed: " + str(end - start))
        driver.quit()
    except:
        driver.quit()


