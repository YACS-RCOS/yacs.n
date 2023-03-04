from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import json

browser = webdriver.Chrome()
action = ActionChains(browser)
# login
browser.get('http://catalog.rpi.edu/preview_program.php?catoid=24&poid=6427&returnto=604')
time.sleep(1)
f = open('jsons/gamesimu.json', 'w', encoding='utf-8')

result = {
    "Major": "Environmental Science",
    "Y1": "First Year",
    "Y1S1": ["Fall"],
    "Y1S2": ["Spring"],
    "Y2": "Second Year",
    "Y2S1": ["Fall"],
    "Y2S2": ["Spring"],
    "Y3": "Third Year",
    "Y3S1": ["The Arch Semester"],
    "Y3S2": ["Fall or Spring"],
    "Y4": "Fourth Year",
    "Y4S1": ["Fall"],
    "Y4S2": ["Spring"]
}
# First Year and Second Year
for i in range(1, 5):
    key = "Y" + str(i) + "S1"
    print(str(i) + " Fall: ")
    fall = browser.find_elements(By.XPATH, "//div[@class='custom_leftpad_20']/div[@class='acalog-core'][" + str(i) +
                                 "]/h2/../following::div[1]/div[1]/ul/li")
    pre = ""
    opt = False
    for j in fall:
        temp = j.text
        if temp.find("\n") != -1:
            temp = temp[:temp.find("\n")]
        if temp.find("(See") != -1:
            continue
        if opt == True:
            result[key][len(result[key])-1] += "   OR   "
            result[key][len(result[key])-1] += temp
            pre = temp
            opt = False
            print("or "+ temp)
            continue
        if(temp == "or" or  temp == "OR"):
            opt = True
            continue
            
        result[key].append(temp)
        print(temp)
        pre = temp
        

    print("")

    key = "Y" + str(i) + "S2"
    print(str(i) + " Spring: ")
    spring = browser.find_elements(By.XPATH, "//div[@class='custom_leftpad_20']/div[@class='acalog-core'][" + str(i) +
                                   "]/h2/../following::div[1]/div[2]/ul/li")
    
    pre = ""
    opt = False
    for j in spring:
        temp = j.text
        if temp.find("\n") != -1:
            temp = temp[:temp.find("\n")]
        if temp.find("(") != -1:
            continue
        if opt == True:
            result[key][len(result[key])-1] += "   OR   "
            result[key][len(result[key])-1] += temp
            pre = temp
            opt = False
            print("or "+ temp)
            continue
        if(temp == "or" or  temp == "OR"):
            opt = True
            continue
        
        
        result[key].append(temp)
        print(temp)

   

print("\nJSON: ")
print(result)
json.dump(result, f)