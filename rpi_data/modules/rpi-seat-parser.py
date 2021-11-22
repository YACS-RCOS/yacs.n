import requests
from bs4 import BeautifulSoup

starting_semester = "01" #change to the semester you want to parse (01 == spring, 09 == fall, 05 == summer)
year = "2022"
crnList = ["60366"] #TODO should be an array of strings
for crn in crnList:
    url = "https://sis.rpi.edu/rss/bwckschd.p_disp_detail_sched?term_in="+year+starting_semester+"&crn_in="+crn
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tableFull = soup.find("table", class_="datadisplaytable")               #SIS has a table containing the data for all of the page
    tableOpenings = tableFull.find("table", class_="datadisplaytable")      #And then a table containing the data for seats remaining
    #extract seat values (still need to use .text on vars since this comes with tags)
    capacity = tableOpenings.find_next(class_="dddefault").text
    actual = capacity.find_next(class_="dddefault")
    remaining = actual.find_next(class_="dddefault")
    print(capacity.text)
    print(actual.text)
    print(remaining.text)

