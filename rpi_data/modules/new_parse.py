import requests
from bs4 import BeautifulSoup as bs
import pdb
#from lxml, based on the code from the quacs scraper and the other scraper, we will prob need to parse xml markup
# URL = "https://sis.rpi.edu"

# login = input("Input Your User: ")
# password = input("Input Your Password: ")

# with requests.session() as s:
#     req = s.get(URL).text
#     html = bs(req, "html.parser")
#     token = html.find("input", {"name" : "csrf_token"}).attrs["value"]
#     payload = {
#         "csrf_token" : token,
#         "j_username" : login,
#         "j_password" : password,
#         "_eventId_proceed" : ""
#     }
    
#     res = s.post(URL, data = payload)
#     new_req = s.get(s.url).text
    
#     token = html.find("input")
#Given a semster, eg 202201, and a subject, eg CSCI
#return a list of all the course codes of a dept, maybe more later on.
#sem - year + (spring:01, fall:09, arch:05, winter:12)
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
    print(len(codes))
    
    for text in codes:
        #text is a long attribute tag, but we don't need all of it.
        #The text is returned as: CSCI 1100 Computer... but we only need the course code, or the 5-9th characters
        allCodes.append(text.text[5:9])
    #However this returns text if there is an a tag that isn't a course code
    #Such as CS1, which has an a tag which lists all of the sections of CS1, but only some classes have
    #this tag, because why not
    #So we need to get rid of these strings
    for i in range(allCodes.count("re")):
        allCodes.remove("re")
    return allCodes
#Given a list of the codes, get the relevent information about each course
#This includes things such as CRN, seats and seats per section, times, location, etc
def stuff(allCodes, semester):
    for code in allCodes:
        stuff2(code, semester)
        
def stuff2(code, semester):
    url = "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse?term_in=202209&subj_in=CSCI&crse_in={code}&schd_in=L"
    session = requests.Session()
    webres = session.get(url)
    page = webres.content
    soup = bs(page, "html.parser")
    table = soup.find('table', class_='datadisplaytable')
    #There are two types of table rows in the table, titles, which hold the links to sections
    #as well as the CRNS, and defaults, which hold the credits, times, days, and locations
    
def main():
    allCodes = getCoursesInMajor("202201", "CSCI")
main()