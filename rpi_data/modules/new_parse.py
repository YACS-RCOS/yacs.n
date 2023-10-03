import requests
from bs4 import BeautifulSoup as bs
#from lxml, based on the code from the quacs scraper and the other scraper, we will prob need to parse xml markup
URL = "https://sis.rpi.edu"

login = input("Input Your User: ")
password = input("Input Your Password: ")

with requests.session() as s:
    req = s.get(URL).text
    html = bs(req, "html.parser")
<<<<<<< Updated upstream
    token = html.find("input", {"name" : "csrf_token"}).attrs["value"]
    payload = {
        "csrf_token" : token,
        "j_username" : login,
        "j_password" : password,
        "_eventId_proceed" : ""
    }
    
    res = s.post(URL, data = payload)
    new_req = s.get(s.url).text
    
=======
    token = html.find("input")
def getCoursesInMajor():
    #example, cs courses, will have to generalize later
    #schema for sis links
    #term_in = year + (spring:01, fall:09, arch:05, winter:12)
    #sel_sub = 4 letter course code
    #These two things should be all we need to change
    #though we will need some way to change the course codes later on

    link = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses?term_in=202209&call_proc_in=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&sel_subj=CSCI"
    s = requests.Session()
    webpage_response = s.get(link)
    webpage = webpage_response.content
    soup = BeautifulSoup(webpage, "html.parser")
    
>>>>>>> Stashed changes
