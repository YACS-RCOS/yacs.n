# py get-pip.py
# pip install requests
# pip install bs4
# pip install selenium


import requests
import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs

URL = "http://sis.rpi.edu"

driver = webdriver.Chrome()
driver.get(URL)
driver.implicitly_wait(1)
username_box = driver.find_element(by=By.NAME, value = "j_username")
password_box = driver.find_element(by=By.NAME, value = "j_password")
submit = driver.find_element(by=By.NAME, value = "_eventId_proceed")
username = input("Enter Username: ")
password = input("Enter Password: ")
username_box.send_keys(username)
password_box.send_keys(password)
submit.click()
time.sleep(5)