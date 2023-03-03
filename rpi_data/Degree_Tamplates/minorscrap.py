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
    
    #find the first h1 which is the major name
    title_element = soup.find("h1", id="acalog-content")
    outFile.write(minor_element.text)
    minor = minor_element.text
    outFile.write(":\n")
    startScrap = False
    #the entire class template has a custom leftpad of 20 consistently, so gather that data
    clp20 = soup.find_all(class_ = "custom_leftpad_20")
    cur_entry = ("","")
    startScrap = False #set to true if we have reached the "Program requirements" information
    for items in clp20:
        state = 'newMajor'
        for div in items.find_all("div", recursive = False):
            if (div.text == "Program Requirements" ):
                startScrap = True
        for ultag in sem.find_all("ul"):
            for litag in ultag.find_all("li"):
                if not (len(litag.text) < 4 or litag.text[:4] == "(See"):
                # have < 4 so that 'and' and 'or' statement are not recorded
                    outFile.write("   Course: ")
                    major_db[cur_entry][semName.text].append(litag.text)
                    outFile.write(litag.text)
                    outFile.write("\n")