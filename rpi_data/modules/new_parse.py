import requests
from bs4 import BeautifulSoup as bs

URL = "https://sis.rpi.edu"

login = input("Input Your User: ")
password = input("Input Your Password: ")

with requests.session() as s:
    req = s.get(URL).text
    html = bs(req, "html.parser")
    token = html.find("input", {"name" : "csrf_token"}).attrs["value"]
    payload = {
        "csrf_token" : token,
        "j_username" : login,
        "j_password" : password,
        "_eventId_proceed" : ""
    }
    
    res = s.post(URL, data = payload)
    new_req = s.get(s.url).text
    
