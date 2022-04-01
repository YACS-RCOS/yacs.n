#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 17:40:34 2021

@author: ziweipeng
"""

import requests
from bs4 import BeautifulSoup

#function that takes in text and executes edge case parsing on it, returning the parsed version
def parseText(text):
    #lowercase to avoid "See" vs "see" conflicts
    lowercase_text = text.lower()
    if (len(lowercase_text) > 16 and lowercase_text[:16] == "credits / units:"):
        return ""
    text_to_add = text
    
    #parse out any whitespace from the text_to_add (&nbsp from start)
    text_to_add = text_to_add.strip()
    
    #skips cases that have just empty whitespace in its own litag
    if (text_to_add == ""):
        return ""

    #skips a lone "or" in an litag
    if (lowercase_text == "or"):
        return ""

    #remove descriptive things about courses from being courses themselves
    if (lowercase_text.find("this course") != -1 or lowercase_text.find("defer") != -1):
        return ""

    #if the text has the word "see" in it
    if (lowercase_text.find("see") != -1):
        #skips case that contains "and"/"or" or course listing that starts with "see"
        if (lowercase_text[1:4] == "see" or len(lowercase_text) < 4):
            return ""

        #footnote is at the end of the course name, so remove from "(see" and on
        delete_position = lowercase_text.find("see")-2
        text_to_add = text_to_add[0:delete_position]

    #remove unnecessary spaces inside the text itself
    if (lowercase_text.find("  ") != -1 or lowercase_text.find("\t") != -1):
        text_to_add = ' '.join(text_to_add.split())

    return text_to_add

#function that parses html page and stores major information in major_db
def scrapFromURL(webLink, major_db):    
    URL = webLink
    page = requests.get(URL) 

    #gather the html tree as the soup object
    soup = BeautifulSoup(page.content, "html.parser") 
    
    #find the first h1 which is the major name
    title_element = soup.find("h1", id="acalog-content")
    majorOutFile.write(title_element.text)
    major = title_element.text
    majorOutFile.write(":\n")

    #the entire class template has a custom leftpad of 20 (semi-consistently), so gather that data
    clp20 = soup.find_all(class_ = "custom_leftpad_20")
    cur_entry = ("","")
    startScrap = False #set to true if we have reached the first year information
    academicYear = False

    for items in clp20:
        state = 'newMajor'
        for div in items.find_all("div", recursive = False):
            if (div.text.lower() == "first year"):
                startScrap = True
            #edge case where first year is written as "academic year"
            elif (div.text.lower() == "academic year i"):
                startScrap = True
                academicYear = True
            
            #we've navigated through the divs until the First Year which will be followed by all classes
            if(startScrap):
                #if we arent at the last year's data 
                if state == 'newMajor' or state =="newYear":
                    majorOutFile.write(" Year: ")

                    #parse year data
                    if not academicYear: #common case
                        yearText = div.text.split()[0] + " Year"
                    else:
                        yearText = div.text

                    cur_entry = (major, yearText)

                    #initialize a database entry that is a pair of major and year
                    major_db[cur_entry] = {}
                    majorOutFile.write(yearText)

                    state = 'regularYear'
                    if yearText == "Fourth Year" or yearText == "Academic Year IV":
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
                                    text_to_add = parseText(litag.text)
                                    if (text_to_add == ""):
                                        continue

                                    #merge multiple class options into one class to store in the db
                                    print(text_to_add)
                                    if text_to_add.lower().find("of the following") != -1:
                                        for litag in ultag.find_all("li"):
                                            print("\n\nyo im here\n")
                                            #get the new text and parse it before adding it in
                                            newtext = litag.text
                                            newParsedText = parseText(newtext)
                                            if (newParsedText == ""):
                                                continue
                                            text_to_add += "or {} ".format(newParsedText)

                                    #the text has been confirmed to be a class and it has been parsed as well so add
                                    majorOutFile.write("   Course: ")
                                    major_db[cur_entry][semName.text].append(text_to_add)
                                    majorOutFile.write(text_to_add)
                                    majorOutFile.write("\n")
                            #is there another edge case where some are not in ul or li                                        
                        
                        else:
                            # edge case where it is leftpad20
                            for h3 in sem.find_all("h4"):
                                if h3.text == "Culminating Experience":
                                    majorOutFile.write("   Course: Culminating Experience ")    
                            for em in sem.find_all("em"):
                                if em.text[:13] == "Credit Hours:":
                                    majorOutFile.write(em.text + "\n") 
                                    break  

                                               
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
majorOutFile = open("majorTemplate.txt", "a") #append mode
majorOutFile.truncate(0) #resizes the outfile to have 0 bytes effectively emptying it

for link in f:
    #print(link, end="")
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
    # temporary solution to solve edge case where years for majors don't have semesters = 2
    if len(major_db[major_year].keys()) != 2:
        continue
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

#for item in major_db.keys():
    #print("\n{}: {}\n".format(item, major_db[item]))
