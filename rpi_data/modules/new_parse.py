#!/usr/bin/env python
import time
import copy
from concurrent.futures import ThreadPoolExecutor
import sys
from bs4 import BeautifulSoup as bs
import pandas as pd
import pdb
import requests
import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from course import Course
import headless_login as login
#from lxml, based on the code from the quacs scraper and the other scraper,
# we will prob need to parse xml markup
#term format: spring2023, fall2023, summer2023, hartford2023, enrichment2023
#TROUBLESHOOTING: remove the line "options.add_argument("--headless")"
# to see where the script might be stalling
#TROUBLESHOOTING: If DUO changes their website the parser will break 
# (but in an easy to fix way, like by adding an extra button click) SIS
# hasn't been substantially changed since 2006 so it probably won't be changed any time soon.
#The sisCourseSearch function serves a similar purpose as the courseUpdate
# function, so if you make any changes to the the top half of either (before the for loop),
# try to do it for both

def gen_base_value(term): #this function returns the code sis uses for a specific term
    basevalue = 200000 #this number will represent the term we are looking at
    while True: #this will add the term code to the last digit, making sure that the term exists
        try:
            # add the month value
            if "spring" in term:
                basevalue += 1
            elif "fall" in term:
                basevalue += 9
            elif "summer" in term:
                basevalue += 5
            elif "hartford" in term:
                basevalue += 10
            elif "enrichment" in term:
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

def sis_course_search(driver, term):
    """
    main loop of the parser, goes to the course search, selects the desired term, 
    and then loops through each subject to grab the course tables
    """
    info = []
    course_codes_dict = find_all_subject_codes(driver)
    url = "https://sis.rpi.edu/rss/bwskfcls.p_sel_crse_search"
    driver.get(url)
    # term selection dropdown
    select = Select(driver.find_element(by=By.ID, value = "term_input_id"))
    basevalue = gen_base_value(term)
    try:
        select.select_by_value(str(basevalue)) # select term based on the basevalue
    except Exception:
        print("The term you entered does not exist.")
        sys.exit()
    # submit term button
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/form/input[2]").click()
    # select subject dropdown
    subject_select = Select(driver.find_element(by=By.XPATH, value = '//*[@id="subj_id"]'))
    subjects = subject_select.options
    subject = ""
    key = str(basevalue)[:4] + "-"
    for i in range(len(subjects)): # loops through all subjects
        start = time.time() # timer to test how long each subject takes
        subject_select.select_by_index(i) # selects a subject
        driver.find_element(by = By.NAME, value = 'SUB_BTN').click() # submits course search
        print("Getting course info")
        courses = get_course_info(driver, key, course_codes_dict) # creates a list of course objects
        with ThreadPoolExecutor(max_workers=50) as pool:
            pool.map(get_req_for_class, courses)
        for i in courses:
            info.append(i)  # appends each course to our final list
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
    #Because we end up sorting in reverse order, reverse the list to get the correct order
    info.reverse()
    return info

def find_all_subject_codes(driver) -> dict():
    #link to a list of schools with their subject codes
    url='https://catalog.rpi.edu/content.php?catoid=26&navoid=670&hl=%22subject%22&returnto=search'
    driver.get(url)
    # We store in a dictionary that has subject code as the key and school as the value
    code_school_dict = dict()
    html = driver.page_source
    soup = bs(html, 'html.parser')
    ptag = soup.find_all('p') # Entire text of page basically
    look_at = []
    for all_things in ptag: # finds all things that are important
        if all_things.find('strong'):
            look_at.append(all_things)
    for all_things in look_at: # in every important part
        school = ""
        for tags in all_things: # look at each school
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
            # uses the current value of school for the dictionary
            # (kind of backwards, but better for our use case)
            code_school_dict[info[0]] = school
    return code_school_dict

def process_special(info, prevrow) -> list[str]:
    """
    For courses that do not have a crn, 99% of the time, these
    will be lab blocks, test blocks, or recitations
    """
    #If this is ever called on an incorrect course.
    #Shouldn't happen but who knows
    if prevrow is None:
        print("course has no crn but first in major")
        return info #Maybe just exit the program instead?
    tmp = format_times(info)
    tmp[18] = format_teachers(tmp[18])
    info = prevrow
    info[6] = tmp[6]
    info[7] = tmp[7]
    info[8] = tmp[8]
    info[12] = tmp[18]
    info[15] = tmp[20]
    return info

def format_teachers(profs : str) -> str:
    """
    Given a string contaings the profs for a class, return a string
    containing only the last names of the profs seperated by a slash.
    """
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

def format_times(info : list[str]) -> list[str]:
    """
    Format the times of the classes into a start and ending time.
    ie 2:00pm-3:50pm becomes 2:00pm as the start time and 3:50pm as the end time
    """
    #Special case where the time is tba or there isn't a valid
    #time see admin 1030 or admin 1100 in spring 2024
    if(info[7] == "TBA" or ':' not in info[7]):
        info.insert(8, "")
        info[7] = ""
        return info
    #Remove any spaces that are in the time. Spaces in the time may cause a csv issue.
    if info[7] != "":
        while " " in info[7]:
            info[7] = info[7].replace(" ", "")
    split_time = info[7].split('-')
    start = split_time[0].upper()
    end = split_time[1].upper()
    if start[0] == '0':
        start = start[1:]
    if end[0] == '0':
        end = end[1:]
    info.insert(7,start)
    info.insert(8,end)
    #Pop to remove original time
    info.pop(9)
    return info

def format_date(info : list, year : str):
    """
    Given the starting and ending date of a class, ie 01/08-04/24,
    turn it into a format the backend likes - 2024-01-08, 2024-04-24
    """
    split_date = info[13].split('-')
    sdate = split_date[0].split('/')
    sdate = '-'.join(sdate)
    enddate = split_date[1].split('/')
    enddate = '-'.join(enddate)
    #Sdate and enddate are the month and days of a semester, eg 01-08 and 05-04
    info.insert(13, year + sdate)
    info.insert(14, year + enddate)
    info.pop(15)

def format_credits(info):
    """
    Turn the credits into an int, pick the greatest credit value
    if there is a range, eg 0.000-16.000 is returned as 16
    """
    if '-' in info[4]:
        return int(float(info[4].split('-')[1]))
    return int(float(info[4]))

def process_row(data: list[str], prevrow: list[str], year: int) -> list[str]:
    """
    Given a row in sis, process the data in said row including crn, course code, days, seats, etc
    Note that we remove a lot of info from the row in SIS, this is to match the format that the
    csv is expecting, see Fall 2023 or any other csv in the repository.
    """
    info = []
    #The first and last elements of the row are useful to us as
    #other parts of the application handle those
    for i in range(1, len(data) - 1, 1):
        #Edge case where the registrar decides to make a column an inconcsistent width.
        #See MGMT 2940 - Readings in MGMT in spring 2024.
        #TODO: Accomodate for colspans different than 2.
        #See https://stackoverflow.com/questions/13263373/beautifulsoup-parsing-tag-table-html-especially-colspan-and-rowspan to start
        if data[i].has_attr("colspan"):
            info.append("TBA")
            info.append("TBA")
        else:
            info.append(data[i].text)
    if len(info) != 21:
        print("Length error in: ")
        print(info[0])
    #info[0] is crn, info[1] is major, 2 - course code, 3- section,
    # 4 - if class is on campus (most are), 5 - credits, 6 - class name
    #info[7] is days, info[8] is time, info[9] is total course capactiy,
    #info[10] is number of students enrolled,
    #info[11] is the number of seats left, info[12] - waitlist capacity,
    #info[13] - waitlist enrolled, info[14] - waitlist spots left,
    #info[15] - crosslist capacity, info[16] - crosslist enrolled,
    #info[17] - crosslist seats left,
    #info[18] are the profs, info[19] are days of the sem that the
    #course spans, and info[20] is location
    #Remove index[4] because most classes are on campus, with
    #exceptions for some grad and doctoral courses.
    info.pop(4)

    #Note that this will shift the above info down by 1 to
    #info[0] crn, info[1]  major, 2 - course code, 3- section, 4 - credits, 5 - class name
    #info[6] is days, info[7] time, info[8] - info[16] actual, 
    #waitlist, and crosslist capacity, enrolled, remaining
    #info[17] profs, info[18] days of sem, and info[19] location
    #The above info is what we are working with for the rest of the method

    #If the crn is empty, then the course is most likely a lab, test,
    # or recitation, so process this row seperately.
    if str(info[0]) == '\xa0':
        info = process_special(info, prevrow)
        return info
    #Some admin and grad courses won't have days of the week
    #Also the backend doesn't like the days of the week being TBA
    if (info[6] == '\xa0' or info[6] == "TBA"):
        info[6] = ""
    #Generally speaking methods that affect info should come in
    #the order that the affect elements, ie
    #time formatitng should come before prof or date
    #formatting because time is at info[6] while date and
    #prof is after. Not doing this can lead to the scraper
    #crashing on some edge cases (see admin 1030 in spring 2024)
    format_times(info)
    #Remove waitlist and crosslist stuff
    info = info[:12] + info[18:]
    #Split the date into start and end date
    format_date(info, year)
    info[12] = format_teachers(info[12])
    #Some classes have a credit value ranging from 0-12, just pick the biggest credit value
    #We do this instead of keeping the range because the backend does not like having a
    #string for the credit value.
    info[4] = format_credits(info)
    return info

def get_str_semester(c : Course) -> str:
    """
    Given a course, return the semester followed by the year, eg if the start date of a
    course is 2024-01-08, then this will return SPRING 2024
    """
    val = str(get_semester(c))
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


def get_course_info(driver, year:str, schools : dict) -> list:
    """
    Given a school year and a dictionary of every major to names of
    their schools, parse all of the info for every course in a major.
    """
    html = driver.page_source
    soup = bs(html, 'html.parser')
    table = soup.find('table', class_='datadisplaytable')
    rows = table.find_all("tr")
    courses = []
    prevrow = []
    for row in rows:
        data = row.find_all("td")
        if len(data) != 0:
            tmp_course = process_row(data, prevrow, year)
            prevrow = copy.deepcopy(tmp_course)
            c = Course(tmp_course)
            c.add_semester(get_str_semester(c))
            if c.major in schools:
                c.add_school(schools[c.major])
            else:
                #A catch all for courses that aren't listed on the
                #offical catalog, such as ADMN or BSUN courses.
                #If in the future there are too many of these were
                #it shouldn't be, then we will have to find a better solution
                c.add_school("Interdisciplinary and Other")
            courses.append(c)
    return courses

def get_req_from_link(webres, course_code, major) -> list:
    """
    Given a url for a course, as well as the course code and major,
    return a list of prereqs, coreqs, and description of the course
    Eg. ITWS 2110 - https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in=202401&subj_code_in=ITWS&crse_numb_in=2110
    Prereqs - ITWS 1100
    Coreqs - CSCI 1200
    Raw -  Undergraduate level CSCI 1200 Minimum Grade of D and
    Undergraduate level ITWS 1100 Minimum Grade of D or Prerequisite Override 100
    Description - This course involves a study of the methods used to extract and
    deliver dynamic information on the World Wide Web.
    The course uses a hands-on approach in which students actively develop Web-based software
    systems. Additional topics include installation, configuration, and management of Web servers.
    Students are required to have access to a PC on which they can install software such
    as a Web server and various programming environments.
    """
    page = webres.content
    soup = bs(page, "html.parser")
    body = soup.find('td', class_='ntdefault')
    #The page is full of \n\n's for some reason, and this nicely splits it into sections
    class_info = body.text.strip('\n\n').split('\n\n')
    for i in range(0,len(class_info),1):
        while '\n' in class_info[i]:
            #Some \n's can make it into the parsed data, so we need to get rid of them.
            class_info[i] = class_info[i].replace('\n','')
    key = "Prerequisites/Corequisites"
    pre_key = "Prerequisite"
    prereqs = ""
    coreqs = ""
    raw = ""
    desc = class_info[0]
    #If the course does not have a description, usually this means that
    #classInfo[0] will be the credit value.
    if desc.strip()[0].isdigit():
        desc = ""
    for i in range(1, len(class_info)):
        if key in class_info[i].strip():
            combo = class_info[i].strip()
            combo = combo[len(key):]
            co_key = "Corequisite"
            if co_key in combo and pre_key in combo:
                coreqs = combo[combo.find(co_key) + len(co_key):]
                prereqs = combo[len(pre_key): combo.find(co_key)]
            elif co_key in combo:
                coreqs = combo[combo.find(co_key) + len(co_key):]
            elif pre_key in combo:
                prereqs = combo[len(pre_key):]
            else:
                #Default case where someone forgets the words we're looking for
                #Note that there are still more edge cases
                #(looking at you csci 6560 and 2110 in spring 2024)
                prereqs = combo
            prereqs = prereqs[prereqs.find(' '):255].strip()
            coreqs = coreqs[coreqs.find(' '):255].strip()
        if class_info[i].strip() == (pre_key + "s:"):
            raw = class_info[i+1].strip()
    ret_list = [prereqs, coreqs, raw, desc]
    return ret_list

def get_req_for_class(course: Course) -> None:
    """
    Add the prereqs for a course to that course
    """
    semester = get_semester(course)
    url = f"https://sis.rpi.edu/rss/bwckctlg.p_disp_course_detail?cat_term_in={semester}&subj_code_in={course.major}&crse_numb_in=course.code{course.code}"
    session = requests.session()
    webres = session.get(url)
    course.add_reqs_from_list(get_req_from_link(webres, course.code, course.major))

def get_semester(course: Course) -> int:
    """
    Given a course, return the basevalue of that course, eg 2024-01 is returned as 202401
    """
    dates = course.sdate.split("-")
    month = dates[1]
    year = dates[0]
    sem = year
    if month in set("08", "09"):
        sem += "09"
    else:
        sem += month
    return sem

def write_csv(info:list, filename: str):
    """
    Given a list of courses, write the courses to a csv specified in the filename
    """
    column_names = ['course_name', 'course_type', 'course_credit_hours',
        'course_days_of_the_week', 'course_start_time', 'course_end_time', 
        'course_instructor', 'course_location', 'course_max_enroll', 'course_enrolled', 
        'course_remained', 'course_department', 'course_start_date', 'course_end_date', 
        'semester', 'course_crn', 'course_level', 'course_section', 'short_name', 'full_name', 
        'description', 'raw_precoreqs','offer_frequency', 'prerequisites', 'corequisites', 
        'school']
    decomposed = [[]] * len(info)
    for i in range(0, len(info), 1):
        decomposed[i] = info[i].decompose()
    df = pd.DataFrame(decomposed, columns = column_names)
    df.to_csv(filename, index=False)

# This main function is helpful for running the full parser standalone,
# without needing environmental variables.

def main():
    options = Options()
    #options.add_argument("--no-sandbox")
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--headless")
    #options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    login.login(driver)
    start = time.time()
    final = sis_course_search(driver, "spring2024")
    end = time.time()
    write_csv(final, "test.csv")
    print("Total Elapsed: " + str(end - start))

#main()
