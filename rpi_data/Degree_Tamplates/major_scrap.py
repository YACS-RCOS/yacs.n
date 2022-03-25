#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 17:40:34 2021

@author: ziweipeng
"""

import requests
from bs4 import BeautifulSoup

outFile = open("pathwayData.txt", "a")
outFile.truncate(0)

def scrapFromURL(webLink, major_db):
    
    URL = webLink
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    ##print(soup)
    

    title_element = soup.find("h1", id="acalog-content")

    outFile.write(title_element.text)
    major = title_element.text
    outFile.write(":\n")

    clp20 = soup.find_all(class_ = "custom_leftpad_20")
    cur_entry = ("","")

    academicYear = False
    startScrap = False
    
    for items in clp20:
        state = 'newMajor'
        for div in items.find_all("div", recursive = False):
            if (div.text.lower() == "first year"):
                startScrap = True
            elif (div.text.lower() == "academic year i"):
                startScrap = True
                academicYear = True

            if(startScrap):
                if state == 'newMajor' or state =="newYear":
                    outFile.write(" Year: ")

                    if not academicYear: #common case
                        yearText = div.text.split()[0] + " Year"
                    else:
                        yearText = div.text

                    cur_entry = (major, yearText)
                    major_db[cur_entry] = {}
                    outFile.write(yearText)
                    state = 'regularYear'

                    if yearText == "Fourth Year" or yearText == "Academic Year IV":
                        state = 'lastYear'
                else:
                    for sem in div.find_all("div", recursive = False):
                        if sem.get("class")[0] != "custom_leftpad_20":
                            outFile.write(sem.get("class")[0] + "\n")
                            semName = sem.find("h3")
                            if semName == None:
                                semName = sem.find("h4")
                            
                            '''
                            for item in major_db.keys():
                                print("{}: {}".format(item, major_db[item]))
                            '''
                            outFile.write("  Sem: ")
                            outFile.write(semName.text)
                            outFile.write("\n")
                            #major_db[cur_entry]["semester"] = semName.text
                            major_db[cur_entry][semName.text] = []

                            for ultag in sem.find_all("ul"):
                                for litag in ultag.find_all("li"):
                                    lowercase_text = (litag.text).lower()
                                    text_to_add = litag.text

                                    #parse out any whitespace from the text_to_add (&nbsp from start)
                                    text_to_add = text_to_add.strip()
                                    
                                    #skips cases that have just empty whitespace in its own litag
                                    if (text_to_add == ""):
                                        continue

                                    #skips a lone "or" in an litag
                                    if (lowercase_text == "or"):
                                        continue

                                    #remove descriptive things about courses from being courses themselves
                                    if (lowercase_text.find("this course") != -1 or lowercase_text.find("defer") != -1):
                                        continue

                                    #if the text has the word "see" in it
                                    if (lowercase_text.find("see") != -1):
                                        #skips case that contains "and"/"or" or course listing that starts with "see"
                                        if (lowercase_text[1:4] == "see" or len(lowercase_text) < 4):
                                            continue

                                        #footnote is at the end of the course name, so remove from "(see" and on
                                        delete_position = lowercase_text.find("see")-2 #-3for the \n\t(
                                        text_to_add = text_to_add[0:delete_position]

                                    #remove unnecessary spaces inside the text itself
                                    if (lowercase_text.find("  ") != -1 or lowercase_text.find("\t") != -1):
                                        text_to_add = ' '.join(text_to_add.split())
                                    
                                    outFile.write("   Course: ")
                                    major_db[cur_entry][semName.text].append(litag.text)
                                    outFile.write(litag.text)
                                    outFile.write("\n")
                        else: 
                            #outFile.write(sem.text + "\n")
                            for h3 in sem.find_all("h4"):
                                if h3.text == "Culminating Experience":
                                    outFile.write("   Course: Culminating Experience ")    
                            for em in sem.find_all("em"):
                                if em.text[:13] == "Credit Hours:":
                                    outFile.write(em.text + "\n") 
                                    break            
                    if state == "lastYear":
                        return major_db
                    state= "newYear"
                
                #outFile.write("count is :{}\n".format(count))
                outFile.write("\n")
    #cleaning1()
    return major_db

major_db = {}
f = open("majorURLlist.txt", "r")
#fout = open("majorData.txt", "w")
i = 0
#scrapFromURL("http://catalog.rpi.edu/preview_program.php?catoid=22&poid=5507&returnto=542", major_db)

for link in f:
    print(link)
    scrapFromURL(link, major_db)

outFile.close()
outFile2 = open("DBCommands.txt", "a")
outFile2.truncate(0)
commandlines = ["","",""]
cmd_sem1 = ""
cmd_sem2 = ""
cmds = []
for major_year in major_db.keys():
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))

    i = 0
    print(major_year)
    print(major_db[major_year].keys())
    for sem in major_db[major_year].keys():
        print(i)
        cmds[i] += "\'{}\',\'{{".format(sem)
        for course in major_db[major_year][sem]:
            cmds[i] += "\"{}\",".format(course)
        cmds[i] = cmds[i][:-1]
        cmds[i] += "}\'),\n"
        i +=1
    for command in cmds:
        outFile2.write(command)
    cmds.clear()
    
outFile2.close()   
        
    


 
for item in major_db.keys():
    print("{}: {}".format(item, major_db[item]))
