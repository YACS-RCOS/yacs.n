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

    pathWayName = soup.find_all(id="acalog-content")

    info = soup.find_all(class_="acalog-core")
    '''
    for course in info:
        #print(course.prettify())
        #outFile.write(course.prettify())
        outFile.write(course.text)
        
        
    for ultag in soup.find_all("ul"):
        for litag in ultag.find_all('li'):
            outFile.write(litag.text)
            outFile.write("\n")
        outFile.write("--------------------\n")
    
    for h3tag in soup.find_all("h3"):
        for ultag in h3tag.find_all("ul"):
            for litag in ultag.find_all('li'):
                outFile.write(litag.text)
                outFile.write("\n")
        outFile.write("--------------------\n")
        '''
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

def cleaning1():
    fin = open("pathwayData.txt", "r").read().replace(
        "\n", " ").replace("\xa0", " ")
    fout = open("pathDataClean11.txt", "a")
    fout.truncate(0)

    importArray = re.split('< |> | Credit Hours: 4|:', fin)
    for info in importArray:
        fout.write(info + "\n")
    fout.write("\n\n\n\n")
    fout.close()
    clean2()


def clean2():
    f = open("pathDataClean11.txt", "r")
    fout = open("ideal.json", "a")
    fout.write('{\n')
    lines = f.readlines()
    i = 0
    required_finished = False
    selective_not_finished = False
    compatible_minor_not_finished = False
    output_string = ""
    for line in lines:
        line = line.strip()
        '''
        if(i == 0):
            output_string += "\"name\":\n\"" + line
        elif("Required" in line):
            output_string += "\",\n\"Required\":[\n"
        elif("Choose" in line):
            output_string = output_string[:-2]
            output_string += "],\n\""+line+"\":[\n"
        elif("Compatible minor" in line):
            output_string = output_string[:-2]
            output_string += "],\n\""+line+"\":\n"
        else:'''
        output_string += "\"" + line + "\",\n"
        i += 1
    output_string = output_string[:-2]
    output_string += "\n}"
    fout.write(output_string)


major_db = {}
scrapFromURL("http://catalog.rpi.edu/preview_program.php?catoid=22&poid=5444&returnto=542", major_db)
for item in major_db.keys():
    print("{}: {}".format(item, major_db[item]))
