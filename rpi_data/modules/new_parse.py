import requests
from bs4 import BeautifulSoup as bs

URL = "https://sis.rpi.edu"

login = input("Input Your User: ")
password = input("Input Your Password: ")

with requests.session() as s:
    req = s.get(URL).text
    html = bs(req, "html.parser")
    token = html.find("input")
    