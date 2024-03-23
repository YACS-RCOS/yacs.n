import requests
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor
from course import Course
from datetime import datetime


def find_codes(term, subj):
    subj_course = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in={}&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj={}".format(term, subj)
    s = requests.Session()
    response = s.get(subj_course)
    webpage = response.content
    soup = bs(webpage, "html.parser")
    table = soup.select("table.datadisplaytable:nth-child(2)")[0]
    elements = table.find_all("td", {"class" : "nttitle"})
    print(len(elements))
    pruned_elements = []
    codes = []
    for all in elements:
        element = all.find("a").text
        pruned_elements.append(element)
        codes.append(element[:9])
    
    return codes
    
def generate_links(term, codes):
    links = []
    for all in codes:
        subj = all[:4]
        code = all[5:]
        single_course = "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse?term_in={}&subj_in={}&crse_in={}&schd_in=L".format(term, subj, code)
        links.append(single_course)
    return links

def scrape_all(links, term):
    courses = []
    with ThreadPoolExecutor(max_workers=50) as pool:
        pool.map(link_scrape, term, links, courses)
    return courses

# info[0] is crn, info[1] is major, 2 - course code, 3- section, 4 - if class is on campus (most are), 5 - credits, 6 - class name 
#info[7] is days, info[8] is time, info[9] is total course capactiy, info[10] is number of students enrolled,
#info[11] is the number of seats left, info[12] - waitlist capacity, info[13] - waitlist enrolled, info[14] - waitlist spots left,
#info[15] - crosslist capacity, info[16] - crosslist enrolled, info[17] - crosslist seats left,
#info[18] are the profs, info[19] are days of the sem that the course spans, and info[20] is location
#Remove index[4] because most classes are on campus, with exceptions for some grad and doctoral courses.  
def link_scrape(term, link, major):
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
        string_element = string_element.replace(body, "")
        if (string_element == str(table_element)):
            print("fail")
        table_element = bs(string_element, "html.parser")
        x += 1
        
        
    if (len(titles) != len(bodies)):
        print("titles do not equal bodies")
    courses = []
    for i in range(len(titles)):
        title = titles[i].text
        split_title = title.split(" - ")        
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
            
        format_and_order(body_info)
    return

def get_slots(term, CRN):
    link = "https://sis.rpi.edu/rss/bwckschd.p_disp_detail_sched?term_in={}&crn_in={}".format(str(term), CRN)
    s = requests.session()
    response = s.get(link)
    webpage = response.content
    soup = bs(webpage, "html.parser")
    info_element = soup.find("div", {"class" : "pagebodydiv"})
    first_table = info_element.find("table")
    table = first_table.find("table")
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
            part = part.strip()
            credits = part
    courses = table_scrape(table)
    for course in courses:
        course.append(credits)
    return courses

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
        final.append(course[2]) # days
        stime, etime = time_split(course[1])
        final.append(stime) # stime
        final.append(etime) # etime
        final.append(course[12]) # max
        final.append(course[13]) # curr
        final.append(course[14]) # rem
        final.append(course[6]) # profs
        sdate, edate = date_split(course[4])
        final.append(sdate) # sdate
        final.append(edate) # edate
        final.append(course[3]) # loc
        print(final)
        new_course = Course(final)
        new_course.addSemester(course[15])
        new_course.print()
        final_courses.append(new_course)
    return final_courses



def time_split(time) -> list[str]:
    split = time.split(" - ")
    if (len(split) != 2):
        raise RuntimeError("Something has gone very wrong in time_split")
    stime = "".join(split[0].split(" ")).upper()
    etime = "".join(split[1].split(" ")).upper()
    return stime, etime

def date_split(date):
    non_formatted = date.split(" - ")
    non_formatted_start = non_formatted[0]
    non_formatted_end = non_formatted[1]
    dt_start = datetime.strptime(non_formatted_start, '%b %d, %Y')
    dt_end = datetime.strptime(non_formatted_end, '%b %d, %Y')
    sdate = "{0:%Y}-{0:%m}-{0:%d}".format(dt_start)
    edate = "{0:%Y}-{0:%m}-{0:%d}".format(dt_end)
    return sdate, edate

    



codes = find_codes(202409, "CSCI")

links = generate_links(202409, codes)

scrape_all(links, "202409")

#link_scrape("202309", "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse?term_in=202309&subj_in=CSCI&crse_in=1200&schd_in=L", "CSCI")

#get_slots(202409, "65029")

#print(number_to_term("202407"))
    
#date_split("Aug 28, 2024 - Dec 20, 2024")

