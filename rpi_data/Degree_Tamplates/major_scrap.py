import logging
from urllib.parse import urljoin
import re
import requests
from bs4 import BeautifulSoup


def scrapFromURL(webLink, major_db):
    
    URL = webLink
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    ##print(soup)
    outFile = open("pathwayData.txt", "a")
    outFile.truncate(0)

    title_element = soup.find("h1", id="acalog-content")

    outFile.write(title_element.text)
    major = title_element.text
    outFile.write(":\n")

    clp20 = soup.find_all(class_ = "custom_leftpad_20")
    cur_entry = ("","")
    for items in clp20:
        count = 0
        for div in items.find_all("div"):
            if count > 14:
                outFile.close()
                return major_db
            if count == 0:
                outFile.write(" Name: ")
                outFile.write(div.text)
            elif count%4 == 1:
                outFile.write(" Year: ")
                cur_entry = (major, div.text)
                major_db[cur_entry] = {}
                outFile.write(div.text)
            else:
                for sem in div.find_all("div"):
                    semName = sem.find("h3")
                    outFile.write("  Sem: ")
                    outFile.write(semName.text)
                    outFile.write("\n")
                    major_db[cur_entry]["semester"] = semName.text
                    major_db[cur_entry]["course"] = []
                    for ultag in sem.find_all("ul"):
                        for litag in ultag.find_all("li"):
                            outFile.write("   Course: ")
                            major_db[cur_entry]["course"].append(litag.text)
                            outFile.write(litag.text)
                            outFile.write("\n")
            
            #outFile.write("count is :{}\n".format(count))
            outFile.write("\n")
            count += 1
             
    outFile.close()
    #cleaning1()
    return major_db

major_db = {}
scrapFromURL("http://catalog.rpi.edu/preview_program.php?catoid=22&poid=5444&returnto=542", major_db)
for item in major_db.keys():
    print("{}: {}".format(item, major_db[item]))
