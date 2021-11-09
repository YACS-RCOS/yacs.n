#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 17:40:34 2021

@author: ziweipeng
"""

import logging
from urllib.parse import urljoin
import re
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

    pathWayName = soup.find_all(id="acalog-content")

    info = soup.find_all(class_="acalog-core")

    clp20 = soup.find_all(class_ = "custom_leftpad_20")
    cur_entry = ("","")
    startScrap = False
    for items in clp20:
        count = 0
        for div in items.find_all("div"):
            if (div.text == "First Year" ):
                startScrap = True
            if(startScrap):
                if count > 13:
                    
                    return major_db
                elif count%4 == 0:
                    outFile.write(" Year: ")
                    yearText = div.text.split()[0] + " Year"
                    cur_entry = (major, yearText)
                    major_db[cur_entry] = {}
                    outFile.write(yearText)
                else:
                    for sem in div.find_all("div"):
                        if sem.get("class")[0] != "custom_leftpad_20":
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
                            major_db[cur_entry][semName.text] = []
                            for ultag in sem.find_all("ul"):
                                for litag in ultag.find_all("li"):
                                    if not (len(litag.text) < 4 or litag.text[:4] == "(See"):
                                    # have < 4 so that 'and' and 'or' statement are not recorded
                                        outFile.write("   Course: ")
                                        major_db[cur_entry][semName.text].append(litag.text)
                                        outFile.write(litag.text)
                                        outFile.write("\n")
                
                #outFile.write("count is :{}\n".format(count))
                outFile.write("\n")
                count += 1
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
'''
for item in major_db.keys():
    fout.write("{}: {}".format(item, major_db[item]))
    fout.write()
    #print("{}: {}".format(item, major_db[item]))
'''
 
for item in major_db.keys():
    print("{}: {}".format(item, major_db[item]))
outFile.close()