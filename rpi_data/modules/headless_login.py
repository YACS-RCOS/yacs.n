import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import time
import os
import sys

def login(driver):
    URL = "http://sis.rpi.edu"
    driver.get(URL) # uses a selenium webdriver to go to the sis website, which then redirects to the rcs auth website
    driver.implicitly_wait(.5)
    username_box = driver.find_element(by=By.NAME, value = "j_username") # creates a variable which contains an element type, so that we can interact with it, j_username is the username text box
    password_box = driver.find_element(by=By.NAME, value = "j_password") # j_password is the password box
    submit = driver.find_element(by=By.NAME, value = "_eventId_proceed") # _eventId_proceed is the submit button
    username = os.environ.get("rcsid", "NONEFOUND")
    password = os.environ.get("rcspw", "NONEFOUND")
    if (username == "NONEFOUND" or password == "NONEFOUND"):
        print("username or password not found, check environment variables")
        sys.exit()
    username_box.send_keys(username) # enters the username
    password_box.send_keys(password) # enters the password
    submit.click() # click the submit button
    while ("duosecurity" not in driver.current_url): # if you entered details incorrectly, the loop will be entered as you aren't on the duo verfication website (redo what we did before)
        print("User or Password Incorrect.")
        username_box = driver.find_element(by=By.NAME, value = "j_username") # we have to redefine the variables because the webpage reloads
        password_box = driver.find_element(by=By.NAME, value = "j_password")
        submit = driver.find_element(by=By.NAME, value = "_eventId_proceed")
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        username_box.clear() # the username box by default has your previous username entered, so we clear it
        username_box.send_keys(username)
        password_box.send_keys(password)
        submit.click()
    while len(driver.find_elements(By.XPATH, '/html/body/div/div/div[1]/div/div[2]/div[3]'))==0:
        time.sleep(.1)
    print("Your DUO code: "+ driver.find_element(by= By.XPATH, value = "/html/body/div/div/div[1]/div/div[2]/div[3]").text)
    
    
    while len(driver.find_elements(By.XPATH, '//*[@id="trust-browser-button"]'))==0:
        time.sleep(.1)
    trust_button = driver.find_element(By.XPATH, '//*[@id="trust-browser-button"]')
    trust_button.click()
    while (driver.current_url != "https://sis.rpi.edu/rss/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu"): #check that the user has inputted their duo code and that it redirected to the sis main page
        time.sleep(1)
    print("Login Success.")


