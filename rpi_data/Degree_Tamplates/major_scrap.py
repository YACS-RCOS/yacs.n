#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 17:40:34 2021

@author: ziweipeng
"""

import requests
from bs4 import BeautifulSoup

#function that takes in text and executes edge case parsing on it, returning the parsed version
#keepOR is true if we want to keep the word or in (for choosing between multiple classes)
def parseText(text, keepOR):
    #lowercase to avoid "See" vs "see" conflicts
    lowercase_text = text.lower()
    text_to_add = text
    
    #parse out any whitespace from the text_to_add (&nbsp from start)
    text_to_add = text_to_add.strip()
    
    #skips cases that have just empty whitespace in its own litag
    if (text_to_add == ""):
        return ""

    #skips a lone "or" in an litag
    if (not keepOR and lowercase_text == "or"):
        return ""

    if (lowercase_text.find("units") != -1):
        return ""

    #case of just "and" in the chemE
    if (lowercase_text == "and"):
        return ""

    #remove descriptive things about courses from being courses themselves
    if (lowercase_text.find("this course") != -1 or lowercase_text.find("defer") != -1):
        return ""

    #if the text has the word "see" in it
    if (lowercase_text.find("see") != -1):
        #skips case of course listing that starts with "see"
        if (lowercase_text[1:4] == "see" or len(lowercase_text) < 4):
            return ""

        #footnote is at the end of the course name, so remove from "(see" and on
        delete_position = lowercase_text.find("see")-2
        text_to_add = text_to_add[0:delete_position]

    #remove unnecessary spaces inside the text itself
    if (lowercase_text.find("  ") != -1 or lowercase_text.find("\t") != -1):
        text_to_add = ' '.join(text_to_add.split())

    return text_to_add

def handleCSE(cur_entry):
    for i in range(2):
        majorOutFile.write("  Sem: ")
        if (i == 0):
            majorOutFile.write("Fall\n")
            major_db[cur_entry]["Fall"] = []

            major_db[cur_entry]["Fall"].append("ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1")
            majorOutFile.write("   Course: ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1\n")

            major_db[cur_entry]["Fall"].append("Computer Engineering Elective Credit Hours: 3-4​")
            majorOutFile.write("   Course: ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 3-4\n")

            major_db[cur_entry]["Fall"].append("Restricted Elective Credit Hours: 3-4​")
            majorOutFile.write("   Course: Restricted Elective Credit Hours: 3-4\n")

            major_db[cur_entry]["Fall"].append("Restricted Elective Credit Hours: 3-4​")
            majorOutFile.write("   Course: Restricted Elective Credit Hours: 3-4\n")

            major_db[cur_entry]["Fall"].append("Technical Elective Credit Hours: 3-4​")
            majorOutFile.write("   Course: Technical Elective Credit Hours: 3-4\n")

        else:
            majorOutFile.write("Spring\n")
            major_db[cur_entry]["Spring"] = []

            major_db[cur_entry]["Spring"].append("ECSE 4900 - Multidisciplinary Capstone Design Credit Hours: 3")
            majorOutFile.write("   Course: ECSE 4900 - Multidisciplinary Capstone Design Credit Hours: 3\n")

            major_db[cur_entry]["Spring"].append("HASS Core Elective Credit Hours: 4")
            majorOutFile.write("   Course: HASS Core Elective Credit Hours: 4\n")

            major_db[cur_entry]["Spring"].append("Free Elective: 3-4​")
            majorOutFile.write("   Course: Free Elective\n")

            major_db[cur_entry]["Spring"].append("Free Elective: 3-4​")
            majorOutFile.write("   Course: Free Elective\n")

            major_db[cur_entry]["Spring"].append("Free Elective: 3-4​")
            majorOutFile.write("   Course: Free Elective\n")

def handleEE(cur_entry):
    for i in range(2):
        majorOutFile.write("  Sem: ")
        if (i == 0):
            majorOutFile.write("Fall\n")
            major_db[cur_entry]["Fall"] = []

            major_db[cur_entry]["Fall"].append("Laboratory Elective Credit Hours: 3")
            majorOutFile.write("   Course: Laboratory Elective Credit Hours: 3\n")

            major_db[cur_entry]["Fall"].append("Restricted Electives: 3-4​")
            majorOutFile.write("   Course: Restricted Electives Credit Hours: 3-4\n")

            major_db[cur_entry]["Fall"].append("Restricted Elective Credit Hours: 3-4​")
            majorOutFile.write("   Course: Restricted Elective Credit Hours: 3-4\n")

            major_db[cur_entry]["Fall"].append("Technical Elective Credit Hours: 3-4​")
            majorOutFile.write("   Course: Technical Elective Credit Hours: 3-4\n")

            major_db[cur_entry]["Fall"].append("HASS Core Electives Credit Hours: 4")
            majorOutFile.write("   Course: HASS Core Electives Credit Hours: 4\n")

        else:
            majorOutFile.write("Spring\n")
            major_db[cur_entry]["Spring"] = []

            major_db[cur_entry]["Spring"].append("ECSE 4900 - Multidisciplinary Capstone Design Credit Hours: 3")
            majorOutFile.write("   Course: ECSE 4900 - Multidisciplinary Capstone Design Credit Hours: 3\n")

            major_db[cur_entry]["Spring"].append("ECSE 2210 - Microelectronics Technology Credit Hours: 3")
            majorOutFile.write("   Course: ECSE 2210 - Microelectronics Technology Credit Hours: 3\n")

            major_db[cur_entry]["Spring"].append("Free Elective: 3-4​")
            majorOutFile.write("   Course: Free Elective: 3-4​\n")

            major_db[cur_entry]["Spring"].append("Free Elective: 3-4​")
            majorOutFile.write("   Course: Free Elective: 3-4​\n")

            major_db[cur_entry]["Spring"].append("ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1")
            majorOutFile.write("   Course: ENGR 4010 - Professional Development: Leadership Competencies Credit Hours: 1\n")

def courseChoiceParse(element):
    resStr = ""
    for ultag in element.find_all("ul"):
        for litag in ultag.find_all("li"):
            #Solves edge case where extra info for a course is put in a separate <li> 
                #tag which messes with appending all course choices by addin an unnecessary OR
            if litag.text.lower().find("[intended to be taken for 4 credit hours]") != -1:
                continue
            if len(resStr) > 0:
                resStr += "OR {}".format(litag.text)
            else:
                resStr += litag.text
    
    #print("resStr", resStr)
    return resStr

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
                        if (yearText == "Courses transferred from Albany Medical College"):
                            #done with physician-scientist so return
                            return
                    cur_entry = (major, yearText)

                    #initialize a database entry that is a pair of major and year
                    major_db[cur_entry] = {}
                    majorOutFile.write(yearText)

                    state = 'regularYear'
                    if yearText == "Fourth Year" or yearText == "Academic Year IV" and major != "Architecture":
                        state = 'lastYear'

                    #case of 5 year architecture program
                    if major == "Architecture" and yearText == "Fifth Year: ":
                        state = 'lastYear'
                else:
                    #no split of semesters like in computer systems engineering
                    if (len(div.find_all("div")) == 0):
                        #confirm that we are the systems engineering major, because this happens for more than one major/////////////////////
                        if (major == "Computer and Systems Engineering"):
                            handleCSE(cur_entry)
                        elif (major == "Electrical Engineering"):
                            handleEE(cur_entry)
                        else:
                            majorOutFile.write("no semester divide as major {}".format(major))
                            #engineering core curriculum twice, electrical engineering once
                            
                                
                    for sem in div.find_all("div", recursive = False):
                        if sem.get("class")[0] != "custom_leftpad_20":
                            #individual semester data (some pages are h3 some are h4)
                            semName = sem.find("h3")
                            if semName == None:
                                semName = sem.find("h4")

                            majorOutFile.write("  Sem: ")
                            majorOutFile.write(semName.text)

                            #initialize class entries for cur_entry's semName semester
                            major_db[cur_entry][semName.text] = []
                            for ultag in sem.find_all("ul"):
                                for litag in ultag.find_all("li"):
                                    
                                    # Solves edge case for Music major program page where students are given many options for courses, 
                                    #calls the courseChoiceParse function which returns a string with all course names combined to form one 'course'
                                    text_to_add = parseText(litag.text, False)
                                    if (text_to_add == ""):
                                        continue

                                    #merge multiple class options into one class to store in the db
                                    if text_to_add.lower().find("of the following") != -1:
                                        text_to_add = courseChoiceParse(litag)
                                        print("The text to add is: ", text_to_add)
                                        
                                    if text_to_add.lower()[:2] == "or":
                                        print("found or in", major, "major")
                                        majorOutFile.write(" " + text_to_add + "\n")
                                        continue
                                    
                                    majorOutFile.write("\n")
                                    #the text has been confirmed to be a class and it has been parsed as well so add
                                    majorOutFile.write("   Course: ")
                                    major_db[cur_entry][semName.text].append(text_to_add)
                                    majorOutFile.write(text_to_add)

                            if yearText == "Second Year" and semName.text == "Spring" and major == "Engineering Core Curriculum":
                                #stop after the 2nd year for the Engineering Core Curriculum major
                                majorOutFile.write("\n")
                                return
                            #is there another edge case where some are not in ul or li                                        
                            majorOutFile.write("\n")
                        else:
                            # edge case where it is leftpad20
                            for h4 in sem.find_all("h4"):
                                if h4.text == "Culminating Experience":
                                    majorOutFile.write("   Course: Culminating Experience ")
                                if h4.text.lower().find("choose one:") != -1:
                                    for div in sem.find_all("div"):
                                        #print("div text", div.text)
                                        majorOutFile.write(courseChoiceParse(div))
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
