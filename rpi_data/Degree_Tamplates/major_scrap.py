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
            if (div.text == "First Year"):
                startScrap = True
            elif (div.text == div.text == "Academic Year I"):
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
                            #print(sem.get("class")[0])
                            #print(semName)
                            '''
                            for item in major_db.keys():
                                print("{}: {}".format(item, major_db[item]))
                            '''
                            outFile.write("  Sem: ")
                            outFile.write(semName.text.split()[0])
                            outFile.write("\n")
                            #major_db[cur_entry]["semester"] = semName.text
                            major_db[cur_entry][semName.text] = []
                            for ultag in sem.find_all("ul"):
                                for litag in ultag.find_all("li"):
                                    if not (len(litag.text) < 4 or litag.text[:4] == "(See"):
                                    # have < 4 so that 'and' and 'or' statement are not recorded
                                        outFile.write("   Course: ")
                                        major_db[cur_entry][semName.text].append(litag.text)
                                        outFile.write(litag.text)
                                        outFile.write("\n")
                        else: 
                            for h3 in sem.find_all("h4"):
                                if h3.text == "Culminating Experience":
                                    outFile.write("   Course: Culminating Experience ")    
                            for em in sem.find_all("em"):
                                if em.text[:13] == "Credit Hours:":
                                    outFile.write(em.text + "\n")             
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
#scrapFromURL("http://catalog.rpi.edu/preview_program.php?catoid=22&poid=5333&returnto=542", major_db)

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
    #cmd_sem1 += "(\'{}\', \'{}\',".format(major_year[0], major_year[1])
    #cmd_sem2 = cmd_sem1
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    #outFile2.write("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    i = 0
    for sem in major_db[major_year].keys():
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
