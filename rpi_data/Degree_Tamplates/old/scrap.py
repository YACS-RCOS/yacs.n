import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def scrapFromURL(webLink):
    URL = webLink
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    outFile = open("majorData.txt", "a")
    outFile.truncate(0)

    title_element = soup.find("h1", id="acalog-content")
    outFile.write(title_element.text)
    outFile.write(":\n")

    pathWayName = soup.find_all(id="acalog-content")

    info = soup.find_all(class_="acalog-core")
    for course in info:
        outFile.write(course.text)
    outFile.close()
    cleaning1()


def cleaning1():
    fin = open("majorData.txt", "r").read().replace(
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
    f = open("majorDataClean1.txt", "r")
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
        else:
            output_string += "\"" + line + "\",\n"
        i += 1
    output_string = output_string[:-2]
    output_string += "\n}"
    fout.write(output_string)


fin = open("majorURLlist2022FA.txt", "r")

scrapFromURL("http://catalog.rpi.edu/preview_program.php?catoid=8&poid=1756&returnto=185")
