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
    outFile.write(title_element.text)
    minor = title_element.text
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
outFile.close()
#still need to get the commands text file with the footnote info
outFile2 = open("__", "a")
outFile2.truncate(0)
commandlines = ["","",""]
cmd_sem1= ""
cmds = []
for minor_year in minor_db.keys():
    cmds.append("(\'{}\', \'{}\',".format(minor_year[0], minor_year[1]))
    i = 0
    for sem in minor_db[minor_year].keys():
        cmds[i] += "\'{}\',\'{{".format(sem)
        for course in minor_db[minor_year][sem]:
            cmds[i] += "\"{}\",".format(course)
        cmds[i] = cmds[i][:-1]
        cmds[i] += "}\'),\n"
        i +=1
    for command in cmds:
        outFile2.write(command)
    cmds.clear()
        
outFile2.close() 

