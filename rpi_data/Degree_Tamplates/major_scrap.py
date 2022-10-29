#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 17:40:34 2021

@author: ziweipeng
"""
'''
This file used to read the weblinks from "xxxURLlistxxx.txt" to the another txt file(include all the info on the website)
'''
import requests
from bs4 import BeautifulSoup

#outFile = open("pathwayData.txt", "a") #append mode
outFile = open("majorData2022.txt", "a") #append mode
outFile.truncate(0) #resizes the outfile to have 0 bytes effectively emptying it

def scrapFromURL(webLink, major_db):
    
    URL = webLink
    page = requests.get(URL) 

    #gather the html tree as the soup object
    soup = BeautifulSoup(page.content, "html.parser") 
    #print(soup)
    
    #find the first h1 which is the major name
    title_element = soup.find("h1", id="acalog-content")
    outFile.write(title_element.text)
    major = title_element.text
    outFile.write(":\n")

    #the entire class template has a custom leftpad of 20 consistently, so gather that data
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
                    outFile.write(" Year: ")

                    #parse year data
                    yearText = div.text.split()[0] + " Year"
                    cur_entry = (major, yearText)

                    #initialize a database entry that is a pair of major and year
                    major_db[cur_entry] = {}
                    outFile.write(yearText)

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
                            #print(sem.get("class")[0])
                            #print(semName)
                            '''
                            for item in major_db.keys():
                                print("{}: {}".format(item, major_db[item]))
                            '''
                            outFile.write("  Sem: ")
                            outFile.write(semName.text)
                            outFile.write("\n")
                            #major_db[cur_entry]["semester"] = semName.text

                            #initialize class entries for cur_entry's semName semester
                            major_db[cur_entry][semName.text] = []
                            for ultag in sem.find_all("ul"):
                                for litag in ultag.find_all("li"):
                                    if not (len(litag.text) < 4 or litag.text[:4] == "(See"):
                                    # have < 4 so that 'and' and 'or' statement are not recorded
                                        outFile.write("   Course: ")
                                        major_db[cur_entry][semName.text].append(litag.text)
                                        outFile.write(litag.text)
                                        outFile.write("\n")
                        #else:                     
                    if state == "lastYear":
                        #done reading data so end the scrape   
                        return major_db
                    state= "newYear"
                
                #outFile.write("count is :{}\n".format(count))
                outFile.write("\n")
    #cleaning1()
    return major_db

major_db = {}
#f = open("majorURLlist.txt", "r")
f = open("majorURLlist2022FA.txt", "r") #the updated txt file
#fout = open("majorData.txt", "w")
i = 0
#scrapFromURL("http://catalog.rpi.edu/preview_program.php?catoid=22&poid=5333&returnto=542", major_db)

for link in f:
    #print(link) use to test
    scrapFromURL(link, major_db)

#print(major_db) #use to test

outFile.close()
#outFile2 = open("DBCommands.txt", "a")
#outFile2 = open("DBCCommandsN.txt", "a")
outFile2 = open("a.txt", "a")
outFile2.truncate(0)
commandlines = ["","",""]
cmd_sem1 = ""
cmd_sem2 = ""
cmds = []
#count = 0 #use to debug
#print(major_db.keys) #use to test
#print(major_db.values) #use to test

''' 
debug
for major_year in major_db.keys():
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    count += 1
    cmds.clear()
print(count) #168

'''

for major_year in major_db.keys():
    #cmd_sem1 += "(\'{}\', \'{}\',".format(major_year[0], major_year[1])
    #cmd_sem2 = cmd_sem1
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    cmds.append("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    #outFile2.write("(\'{}\', \'{}\',".format(major_year[0], major_year[1]))
    #print(cmds) #use to test

    '''
    debug
    if (len(cmds) != 0):
        count += 1
        print("true")
        print(count) #107
    '''
    '''
    if (len(cmds) == 0):
        continue
    '''
    i = 0
    for sem in major_db[major_year].keys(): #sem is the semester that will open for the class
        #print(cmds[i]) #use to test
        cmds[i] += "\'{}\',\'{{".format(sem)
        for course in major_db[major_year][sem]:
            cmds[i] += "\"{}\",".format(course)
            #print(course)
        cmds[i] = cmds[i][:-1] #delete the ","
        cmds[i] += "}\'),\n"
        i += 1
    for command in cmds:
        outFile2.write(command)
    cmds.clear()

outFile2.close()   
        
'''   
for item in major_db.keys():
    print("{}: {}".format(item, major_db[item]))
'''
