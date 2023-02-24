import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


def scrapFromURL(webLink):
    URL = webLink
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    outFile = open("minorData.txt", "a")
    outFile.truncate(0)

    title_element = soup.find("h1", id="acalog-content")
    outFile.write(minor_element.text)
    outFile.write(":\n")

    pathWayName = soup.find_all(id="acalog-content")

    info = soup.find_all(class_="acalog-core")
    for course in info:
        outFile.write(minorcourse.text)
    outFile.close()
