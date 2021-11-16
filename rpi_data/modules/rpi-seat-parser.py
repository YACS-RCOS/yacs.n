from bs4 import BeautifulSoup

starting_semester = "01" #change to the semester you want to parse (01 == spring, 09 == fall, 05 == summer)
year = "2021"
crnList = [] #TODO
for crn in crnList:
    url = "https://sis.rpi.edu/rss/bwckschd.p_disp_detail_sched?term_in="+year+starting_semester+"&crn_in="+crn

