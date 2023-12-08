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

# Remember to add enviromental variables named rcsid and rcspw with your account info!!!
#
# THINGS THAT CAN POTENTIALLY GO WRONG HERE AND HOW TO FIX THEM:
# 
# - If the RPI login website changes at all, it's very likely that the login will break. Fixing might involve changing what element selenium looks for.
# - DUO likes to change things. If they implement another 2FA type or add extra buttons for some reason you'll have to add more checks and button presses
# - Selenium errors can occur if your internet is slow or if you have multiple browser instances open, so try to avoid this
# 
# - You need to install firefox (I hate Google Chrome, and you should too). If you change it to be a Chrome instance instead it probably won't work from my experience
# - To fix these things you can comment this line: "options.add_argument("--headless")" in the parse_runner file to see what goes wrong if python doesn't throw anything
# - Try restarting python/vscode or even your computer if it's throwing something really weird for no reason
# - You can try sending me a message on discord @gcm as a last resort


def login(driver):
    URL = "http://sis.rpi.edu"
    driver.get(URL) # uses a selenium webdriver to go to the sis website, which then redirects to the rcs auth website
    username_box = driver.find_element(by=By.NAME, value = "j_username") # creates a variable which contains an element type, so that we can interact with it, j_username is the username text box
    password_box = driver.find_element(by=By.NAME, value = "j_password") # j_password is the password box
    submit = driver.find_element(by=By.NAME, value = "_eventId_proceed") # _eventId_proceed is the submit button
    username = os.environ.get("rcsid", "NONEFOUND")
    password = os.environ.get("rcspw", "NONEFOUND")
    if (username == "NONEFOUND" or password == "NONEFOUND"):
        print("username or password not found, check environment variables or input them manually")
        username = input("Enter username: ")
        password = input("Enter password: ")
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
    while len(driver.find_elements(By.XPATH, '/html/body/div/div/div[1]/div/div[2]/div[7]/a'))==0:
        time.sleep(.1)
    options  = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[2]/div[7]/a')
    options.click()
    while len(driver.find_elements(By.XPATH, '/html/body/div/div/div[1]/div/div[1]/ul/li[1]/a')) == 0:
        time.sleep(.1)
    duo_option = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[1]/ul/li[1]/a')
    duo_option.click()
    while len(driver.find_elements(By.XPATH, '/html/body/div/div/div[1]/div/div[2]/div[3]')) == 0:
        time.sleep(.1)
    print("Your DUO code: "+ driver.find_element(by= By.XPATH, value = "/html/body/div/div/div[1]/div/div[2]/div[3]").text) # print the duo code
    while len(driver.find_elements(By.XPATH, '//*[@id="trust-browser-button"]'))==0: # we need to press the trust browser button, so we wait until that shows up
        time.sleep(.1)
    trust_button = driver.find_element(By.XPATH, '//*[@id="trust-browser-button"]') #find and click it
    trust_button.click()
    time.sleep(3)
    if (driver.current_url == "https://sis.rpi.edu/rss/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu"): # check if we're in the right place
        return "Success"
    else:
        print("login failed")
        return "Failure"
