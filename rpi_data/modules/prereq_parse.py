#Ok so this file should take in some inputs (what though) and output a dictionary.
#This dictionary has all of the courses' crn as the keys and the value as the relevant information
#See fetch_catalog_course_info.py for the source of a lot of the code
#It's just that I will be rewriting it so that it is (hopefully) more understandable and better documented
import requests as req
import threading #https://docs.python.org/3/library/threading.html
import unicodedata
import re
import regex #https://www.dataquest.io/blog/regex-cheatsheet/
import json 
from datetime import date
from time import time
from threading import Lock
from io import StringIO
from bs4 import BeautifulSoup, SoupStrainer #https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from lxml import etree
import pdb

#Though we probably will not need everything here
class PrereqParse:
    def __init__(self, api_key):
        self.key = api_key
        self.search_endpoint = "http://rpi.apis.acalog.com/v2/search/courses"
        self.course_detail_endpoint = "http://rpi.apis.acalog.com/v2/content?options[full]=1&method=getItems&type=courses"
        self.catalogIdEndpoint = "http://rpi.apis.acalog.com/v2/content?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml&method=getCatalogs"
        self.resFormat = "xml"
        self.catalogId = 0
        self.lock = Lock()
        self.courseDetailsXMLStr = []
        self.xmlProlog = ""
        self.catalogRoot = ""
        self.chunkSize = 100
        self.courses = dict()
    #Returns the current catalog id for the specified year
    def getCataId(self, year : int):
        res = req.get(self.catalogIdEndpoint)
        tree = etree.parse(StringIO(res.content.decode()))
        root = tree.getroot()
        try:
            pdb.set_trace()
            #currentCatalog = root.xpath("//*[local-name() = 'archived'][contains(text(), 'No')]")
            #currentCatalog = root.xpath("//*[local-name() = 'archived']")
            #tree.xpath("//*[local-name() = 'archived']")[0].getparent().getparent().attrib['id']
            #TODO: Rewrite in regex
            #TODO: get the catalog id from this
            retCata = root.xpath("//*[local-name() = 'archived']")[0].getparent().getparent().attrib['id']
            return 0
        except Exception as exception:
            print("Failed to get the catalog id")
    #Return the endpoint of the course ids
    def getCourseIds(self):
        return 0
    #Return a dictionary of every course in the catalog
    def getAllCourses(self):
        return 0
    #Return the details of a single course
    def getCourseDetails(self):
        return 0
    #Runs the program
    def run(self, year):
        #Maybe make some feature to get the catalog for every year?
        self.catalogId = self.getCataId(year)
        ids = self.getCourseIds()
        courses = getAllCourses()

def main():
    parser = PrereqParse("3eef8a28f26fb2bcc514e6f1938929a1f9317628")
    parser.run(2023)
main()