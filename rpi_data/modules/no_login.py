import requests
from bs4 import BeautifulSoup as bs




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

def scrape_all(links):
    return

def link_scrape(link):
    return

codes = find_codes(202409, "CSCI")

links = generate_links(202409, codes)

print(links)