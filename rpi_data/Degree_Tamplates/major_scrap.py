#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 17:40:34 2021

@author: ziweipeng
"""

import requests
from bs4 import BeautifulSoup

#function that parses html page and stores major information in major_db
def scrapFromURL(webLink, major_db):    
    URL = webLink
    page = requests.get(URL) 

    #gather the html tree as the soup object
    soup = BeautifulSoup(page.content, "html.parser") 
    #print(soup)
    
    #find the first h1 which is the major name
    title_element = soup.find("h1", id="acalog-content")
    majorOutFile.write(title_element.text)
    major = title_element.text
    majorOutFile.write(":\n")

    #the entire class template has a custom leftpad of 20 (semi-consistently), so gather that data
    clp20 = soup.find_all(class_ = "custom_leftpad_20")
    cur_entry = ("","")
    startScrap = False #set to true if we have reached the first year information

    for items in clp20:
        state = 'newMajor'
        for div in items.find_all("div", recursive = False):
            if (div.text == "First Year" ):
                startScrap = True
            
            #we've navigated through the divs until the First Year which will be followed by all classes
            if(startScrap):
                #if we arent at the last year's data 
                if state == 'newMajor' or state =="newYear":
                    majorOutFile.write(" Year: ")

                    #parse year data
                    yearText = div.text.split()[0] + " Year"
                    cur_entry = (major, yearText)

                    #initialize a database entry that is a pair of major and year
                    major_db[cur_entry] = {}
                    majorOutFile.write(yearText)

                    state = 'regularYear'
                    if yearText == "Fourth Year":
                        state = 'lastYear'
                else:
                    for sem in div.find_all("div", recursive = False):
                        if sem.get("class")[0] != "custom_leftpad_20":
                            #individual semester data (some pages are h3 some are h4)
                            semName = sem.find("h3")
                            if semName == None:
                                semName = sem.find("h4")

                            majorOutFile.write("  Sem: ")
                            majorOutFile.write(semName.text)
                            majorOutFile.write("\n")

                            #initialize class entries for cur_entry's semName semester
                            major_db[cur_entry][semName.text] = []
                            for ultag in sem.find_all("ul"):
                                for litag in ultag.find_all("li"):
                                    #lowercase to avoid "See" vs "see" conflicts
                                    lowercase_text = (litag.text).lower()
                                    text_to_add = litag.text

                                    #if the text has the word footnote in it
                                    if (lowercase_text.find("footnote") != -1):
                                        #skips case that contains "and"/"or" or starts with "see"
                                        if (lowercase_text[1:4] == "see" or len(lowercase_text) < 4):
                                            #print("Skipping over the case of: " + text_to_add)
                                            continue

                                        #footnote is at the end of the course name, so parse from "(see" and on out
                                        delete_position = lowercase_text.find("see")-3#-3for the \n\t(
                                        text_to_add = text_to_add[0:delete_position]
                                        print("New text_to_add is", text_to_add)

                                    #the text has been confirmed to be a class and it has been parsed as well so add
                                    majorOutFile.write("   Course: ")
                                    major_db[cur_entry][semName.text].append(text_to_add)
                                    majorOutFile.write(text_to_add)
                                    majorOutFile.write("\n")
                            #is there another edge case where some are not in ul or li                                        
                        #else:
                        # edge case where it is leftpad20                     
                    if state == "lastYear":
                        #done reading data so end the scrape  
                        majorOutFile.write("\n")
                        return major_db
                    state= "newYear"
                
                majorOutFile.write("\n")
    #if the for loop never runs
    return major_db

#initialize database dictionary and grab the url file
major_db = {}
f = open("majorURLlist.txt", "r")

#initialize outfile and scrape from each url all the major data
majorOutFile = open("pathwayData.txt", "a") #append mode--------------this shouldnt be named pathway data
majorOutFile.truncate(0) #resizes the outfile to have 0 bytes effectively emptying it

for link in f:
    print(link, end="")
    scrapFromURL(link, major_db)
    #break

#all major info is obtained so close the outfile
majorOutFile.close()

#create outfile that stores sql commands made from the major info
sqlOutFile = open("DBCommands.txt", "a")
sqlOutFile.truncate(0)

commandlines = ["","",""]
cmd_sem1 = ""
cmd_sem2 = ""
cmds = []

for major_year in major_db.keys():
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))

    i = 0
    for sem in major_db[major_year].keys():
        cmds[i] += "\'{}\',\'{{".format(sem)
        for course in major_db[major_year][sem]:
            cmds[i] += "\"{}\",".format(course)
        cmds[i] = cmds[i][:-1]
        cmds[i] += "}\'),\n"
        i += 1
    for command in cmds:
        sqlOutFile.write(command)
    cmds.clear()
        
sqlOutFile.close()   

for item in major_db.keys():
    print("\n{}: {}\n".format(item, major_db[item]))
