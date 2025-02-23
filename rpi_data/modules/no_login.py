import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor
from course import Course
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import multiprocessing
import new_parse as old
import courses_scraper as cs
import ci_scraper as cis
import goldy_parse as gold
import regex as re
import os
import sys

'''
Finds all of the course codes for a given term and subject.
'''
def find_codes(term, subj):
    subj_course = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in={}&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj={}".format(term, subj)
    s = requests.Session()
    response = s.get(subj_course)
    webpage = response.content
    soup = bs(webpage, "html.parser")
    try:
        table = soup.select("table.datadisplaytable:nth-child(2)")[0]
        elements = table.find_all("td", {"class" : "nttitle"})
    except Exception:
        return []
    print(len(elements))
    pruned_elements = []
    codes = []
    for all in elements:
        element = all.find("a").text
        pruned_elements.append(element)
        codes.append(element[:9])
    
    return codes

'''
Generates SIS links for a list of codes
'''
def generate_links(term, codes):
    links = []
    for all in codes:
        subj = all[:4]
        code = all[5:]
        single_course = "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse?term_in={}&subj_in={}&crse_in={}&schd_in=L".format(term, subj, code)
        links.append(single_course)
    return links

'''
Scrapes all of the course information for a list of links.
'''
def scrape_all(links, term, major) -> list[Course]:
    courses = []
    for link in links:
        try:
            temp_courses = link_scrape(term, link, major)
        except Exception:
            print(link)
            raise Exception("Failed Parse")
        
        if (temp_courses == None):
            continue
        for i in temp_courses:
            courses.append(i)

    return courses

# info[0] is crn, info[1] is major, 2 - course code, 3- section, 4 - if class is on campus (most are), 5 - credits, 6 - class name 
#info[7] is days, info[8] is time, info[9] is total course capactiy, info[10] is number of students enrolled,
#info[11] is the number of seats left, info[12] - waitlist capacity, info[13] - waitlist enrolled, info[14] - waitlist spots left,
#info[15] - crosslist capacity, info[16] - crosslist enrolled, info[17] - crosslist seats left,
#info[18] are the profs, info[19] are days of the sem that the course spans, and info[20] is location
#Remove index[4] because most classes are on campus, with exceptions for some grad and doctoral courses. 
'''
Main link scrape, which splits the page into individual courses and then scrapes each.
'''
def link_scrape(term, link, major) -> list[Course]:
    s = requests.Session()
    response = s.get(link)
    webpage = response.content
    soup = bs(webpage, "html.parser")
    info_element = soup.find("div", {"class" : "pagebodydiv"})
    table_element = info_element.find("table")
    tr_tags = table_element.find_all("tr")
    if (len(tr_tags) == 1 and "No classes were found that meet your search criteria" in tr_tags[0].text):
        return None
    titles = table_element.find_all("th", {"class" : "ddtitle"})
    bodies = []
    x = 0
    while (table_element.find("td", {"class" : "dddefault"})):
        bodies.append(table_element.find("td", {"class" : "dddefault"}))
        string_element = str(table_element)
        body = str(bodies[x])
        string_element = string_element.replace(body, "", 1)
        if (string_element == str(table_element)):
            print("fail")
        table_element = bs(string_element, "html.parser")
        x += 1

        
    if (len(titles) != len(bodies)):
        raise RuntimeError("Titles do not equal bodies: "+ link)
    courses = []
    for i in range(len(titles)):
        title = titles[i].text
        split_title = title.rsplit(" - ", 3)        
        body_info = body_scrape(bodies[i])
        slots = get_slots(term, split_title[1])
        for course in body_info:
            course.append(split_title[1]) # CRN
            course.append(split_title[2].split(" ")[1]) # course code
            course.append(split_title[3]) # section
            course.append(major) # major
            course.append(slots[0]) # capacity
            course.append(slots[1]) # current_enrolled
            course.append(slots[2]) # remaining
            course.append(number_to_term(term))
            course.append(split_title[0]) # NAME
        
        formatted = format_and_order(body_info)
        [courses.append(i) for i in formatted]
    return courses

'''
Scrapes the course occupancy information for a specific course from SIS.
'''
def get_slots(term, CRN):
    link = "https://sis.rpi.edu/rss/bwckschd.p_disp_detail_sched?term_in={}&crn_in={}".format(str(term), CRN)
    s = requests.session()
    response = s.get(link)
    webpage = response.content
    soup = bs(webpage, "html.parser")
    info_element = soup.find("div", {"class" : "pagebodydiv"})
    first_table = info_element.find("table")
    table = first_table.find("table")
    if table == None:
        return ["0", "0", "0"]
    scraped_table = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        stripped_row = []
        if columns != []:
            for element in columns:
                stripped_row.append(element.text)
            scraped_table.append(stripped_row)
    scraped_table.pop(0)
    return scraped_table[0]

'''
Scrapes info from main page for a single course.
'''
def body_scrape(body) -> list[list[str]]:
    table = body.find("table")
    string_body = str(body)
    string_body = string_body.replace(str(table), "")
    string_body = string_body.replace("<br>", "")
    string_body = string_body.replace("<br/>", "")
    split_body = string_body.split("\n")
    credits = ""
    for part in split_body:
        if "Credits" in part:
            part = part.replace("Credits", "")
            part = part.replace(".000", "")
            if ("TO" in part):
                temp = part.split("TO")
                temp[0] = temp[0].strip()
                temp[1] = temp[1].strip()
                part = "-".join(temp)

            part = part.strip()
            credits = part
    if table != None:
        courses = table_scrape(table)
    else:
        courses = []
    for course in courses:
        course.append(credits)
    return courses

'''
Scrapes a table element into a 2D string list.
'''
def table_scrape(table:bs) -> list[list[str]]:
    # ["", Type, Time, Days, Where, Date Range, Schedule Type, Instructor]
    scraped_table = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        stripped_row = []
        if columns != []:
            for element in columns:
                stripped_row.append(element.text)
            scraped_table.append(stripped_row)
    return scraped_table

'''
turns a term number into a human readable term
'''
def number_to_term(term) -> str:
    date = term[:4]
    if term[4:] == "01":
        date = "SPRING " + date
    elif term[4:] == "09":
        date = "FALL " + date
    elif term[4:] == "05" or term[4:] == "06" or term[4:] == "07" or term[4:] == "08":
        date = "SUMMER " + date
    elif term[4:] == "12":
        date = "WINTER " + date
    elif term[4:] == "10":
        date = "HARTFORD " + date
    return date

# current order:

# 0: Type, 1: Time, 2: Days, 3: Where, 4: Date Range, 5: Schedule Type, 6: Instructor, 7: Credits, 8: CRN, 9: course code, 10: section, 11: major, 12: capacity, 13: current, 14: rem, 15: term, 16: NAME

# desired order:

#[crn, major, code, section, credits, name, days, stime, etime, max, curr, rem, profs, sdate, enddate, loc]

'''
Formats and orders the courses into the desired order.
'''
def format_and_order(courses:list[list[str]]) -> list[list[str]]:
    final_courses = []
    for course in courses:
        if (len(course) != 17):
            raise RuntimeError("Too many things got parsed")
        final = []
        final.append(course[8]) # CRN
        final.append(course[11]) # major
        final.append(course[9]) # code
        final.append(course[10]) # section
        final.append(course[7]) # credits
        final.append(course[16]) # name
        final.append(course[2].strip()) # days
        stime, etime = time_split(course[1])
        final.append(stime) # stime
        final.append(etime) # etime
        final.append(course[12]) # max
        final.append(course[13]) # curr
        final.append(course[14]) # rem
        course[6] = course[6].replace("(P)", "")
        temp = course[6].split(" ")
        f_temp = []
        for x in range(len(temp)):
            temp[x] = temp[x].strip()
            if (temp[x] == ""):
                continue
            f_temp.append(temp[x])
        professor_list = " ".join(f_temp)
        professors = professor_list.replace(" , ", "/")
        final.append(professors) # profs
        sdate, edate = date_split(course[4])
        final.append(sdate) # sdate
        final.append(edate) # edate
        final.append(course[3]) # loc
        new_course = Course(final)
        new_course.addSemester(course[15])
        new_course.print()
        final_courses.append(new_course)
    return final_courses



def time_split(time) -> list[str]: # format times
    if (time == "TBA"):
        return "", ""
    split = time.split(" - ")
    if (len(split) != 2):
        raise RuntimeError("Something has gone very wrong in time_split")
    stime = "".join(split[0].split(" ")).upper()
    etime = "".join(split[1].split(" ")).upper()
    return stime, etime

def date_split(date): # format dates
    non_formatted = date.split(" - ")
    non_formatted_start = non_formatted[0]
    non_formatted_end = non_formatted[1]
    dt_start = datetime.strptime(non_formatted_start, '%b %d, %Y')
    dt_end = datetime.strptime(non_formatted_end, '%b %d, %Y')
    sdate = "{0:%Y}-{0:%m}-{0:%d}".format(dt_start)
    edate = "{0:%Y}-{0:%m}-{0:%d}".format(dt_end)
    return sdate, edate

'''
Parent function that scrapes all courses for a given term and writes them to a CSV file.
'''
def no_login_scrape(term: str, num_browsers: int):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options) # starter code which uses selenium
    subjects = old.findAllSubjectCodes(driver) # finds all subject codes
    nav, cat = cs.navigate_to_course(driver, term) # finds the navigation and catalog ids, which are each used to build a course search query.
    driver.quit()
    courses = []
    for subject in subjects.keys():
        codes = find_codes(term, subject) # scrapes all of the course codes for a subject from SIS
        links = generate_links(term, codes) # turns the codes into links
        temp_courses = []
        with multiprocessing.Pool(num_browsers) as pool: # uses multiprocessing to scrape all of the SIS info for a subject
            parts = list(cs.split(links, num_browsers))
            temp_courses = pool.starmap(scrape_all, [(part, term, subject) for part in parts])
        temp_courses = [i for sublist in temp_courses for i in sublist] # flattens the list
        [i.addSchool(subjects[subject]) for i in temp_courses] # adds the school to each course
        temp_codes = list(set([i.major + " " + i.code for i in temp_courses]))
        print(len(temp_codes))
        extra_info = pre_req_scrape(temp_codes, nav, cat, num_browsers) # scrapes the extra info off of the catalog website
        for course in temp_courses: # adds the extra info to each course
            if course.short == None:
                print(course)
                continue
            if course.short not in extra_info:
                course.addReqs([], [], "", "")
                course.desc = ""
                course.frequency = ""
                continue
            course.addReqs(extra_info[course.short]["prerequisites"], extra_info[course.short]["corequisites"], extra_info[course.short]["rawprecoreq"], extra_info[course.short]["description"])
            course.frequency = extra_info[course.short]["offered"]["text"]

        [courses.append(i) for i in temp_courses]
    '''
    Check Professor Goldschmidt's information
    '''
    textTerm = number_to_term(term).lower().replace(" ", "")
    gold_courses = gold.get_goldy_info(textTerm)
    for course in courses:
        if course.short.replace("-", " ") in gold_courses:
            add_goldy_info(course, gold_courses[course.short.replace("-", " ")])
            
    # Build the csv
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.abspath(os.path.join(dir_path, os.pardir))
    path = os.path.join(parent, number_to_term(term).lower().replace(" ", "-") + ".csv")
    old.writeCSV(courses, path)
    os.system(f'send_courses_to_api.py {path}')

'''
Scrapes the prerequisites for multiple courses at once.
'''
def pre_req_scrape(codes: list[str], nav:str, cat:str, num_browsers: int):
    all_courses = dict()
    with multiprocessing.Pool(num_browsers) as pool:
        parts = list(cs.split(codes, num_browsers))
        results = pool.starmap(cs.scrape_process, [(part, nav, cat) for part in parts])
    for res in results:
        all_courses.update(res)
    return all_courses

'''
Edits a course using the information from Professor Goldschmidt's website.
'''
def add_goldy_info(course: Course, goldy_info: dict):
    checking = "Prerequisite"
    if checking not in goldy_info.keys():
        checking = "Prerequisites"
    if checking not in goldy_info.keys():
        goldy_info[checking] = ""
    course.pre = re.findall(r'[A-Z]{4} [0-9]{4}', goldy_info[checking])
    if course.desc == "" and "Description" in goldy_info.keys():
        course.desc = goldy_info["Description"]
    if course.profs == "" and "Instructors" in goldy_info.keys():
        course.profs = goldy_info["Instructors"]
    if "Prerequisite" in goldy_info[checking]:
        course.raw = goldy_info[checking]
    else:
        course.raw = "Prerequisites: " + goldy_info[checking]

def get_input():
    if len(sys.argv) != 3:
        sys.exit("Not enough or too many arguments (2 expected)")
    year = sys.argv[2]
    if not year.isdigit():
        sys.exit(f"Invalid year: {year}")
    elif int(year) < 1824 or int(year) > 2100:
        sys.exit(f"Year is too big or too small: {year}")
    semester = sys.argv[1]
    compound = year
    if semester == 'SPRING':
        compound += '01'
    elif semester == 'FALL':
        compound += '09'
    elif semester == 'SUMMER':
        compound += '05'
    elif semester == 'WINTER':
        compound += '12'
    elif semester == 'HARTFORD':
        compound += '10'
    else:
        sys.exit(f"Invalid Semester: {semester}. Valid options are SPRING/FALL/SUMMER/WINTER/HARTFORD")
    return compound

if __name__ == "__main__":
    compound = get_input()
    print(compound)
    no_login_scrape(compound, 15)
    #driver = webdriver.Firefox()
    #print(cs.scrape_single_course(driver, "CSCI", "1100", 202409))
    #print(link_scrape("202409", "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse?term_in=202409&subj_in=CHME&crse_in=4980&schd_in=L", "CHME"))
