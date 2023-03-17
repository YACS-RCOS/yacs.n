import requests
from bs4 import BeautifulSoup

outFile = open("MinorData.txt", "a") #append mode
outFile.truncate(0) #resizes the outfile to have 0 bytes effectively emptying it

def scrapFromURL(webLink, minor_db):
    
    URL = webLink
    page = requests.get(URL) 

    #gather the html tree as the soup object
    soup = BeautifulSoup(page.content, "html.parser") 
    #print(soup)
    
    #find the first h1 which is the minor name
    title_element = soup.find("h1", id="acalog-content")
    outFile.write(minor_element.text)
    minor = minor_element.text
    #the entire class template has a custom leftpad of 20 consistently, so gather that data
    clp20 = soup.find_all(class_ = "custom_leftpad_20")
    cur_entry = ("","")
    startScrap = False

    for items in clp20:
        for div in items.find_all("div", recursive = False):
            if (div.text == "Program Requirements" ):
                startScrap = True
            if(startScrap):
                for ultag in div.find_all("ul"):
                    for litag in ultag.find_all("li"):
                        if not (len(litag.text) < 4 or litag.text[:4] == "(See"):
                        # have < 4 so that 'and' and 'or' statement are not recorded
                            outFile.write("   Course: ")
                            outFile.write(litag.text)
                            minor_db[cur_entry] = []
                            outFile.write("\n")
    return minor_db

minor_db = {}
f = open("MinorURLlist.txt", "r")
#fout = open("MinorData.txt", "w")
i = 0
for link in f:
    print(link)
    scrapFromURL(link, minor_db)

