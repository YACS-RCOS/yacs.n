import requests
from bs4 import BeautifulSoup

def getSeats(starting_semester, year, crnList):
    for crn in crnList:
        url = "https://sis.rpi.edu/rss/bwckschd.p_disp_detail_sched?term_in="+year+starting_semester+"&crn_in="+crn
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tableFull = soup.find("table", class_="datadisplaytable")               #SIS has a table containing the data for all of the page
        tableOpenings = tableFull.find("table", class_="datadisplaytable")      #And then a table containing the data for seats remaining
        #extract seat values (still need to use .text on vars since this comes with tags)
        capacity = tableOpenings.find_next(class_="dddefault")
        actual = capacity.find_next(class_="dddefault")
        remaining = actual.find_next(class_="dddefault")
        return (capacity, actual, remaining)

