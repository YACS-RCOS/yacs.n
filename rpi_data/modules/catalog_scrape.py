from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

def get_course_link(driver: webdriver, term: int) -> str:

    driver.get(main_url)
    dropdown = driver.find_element(by=By.XPATH, value='//*[@id="select_catalog"]')
    navbar = driver.find_element(by=By.XPATH, value='//*[@id="acalog-navigation"]')
    for element in navbar.find_elements(by=By.TAG_NAME, value="div"):
       to_check = element.find_element(by=By.TAG_NAME, value="a")
       if (to_check.text == "Courses"):
           to_check.click()
           return driver.current_url

def get_all_html(driver: webdriver, url: str) -> list[str]:
    maximum_link = int(driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[103]/td/a[12]').text)
    for i in range(maximum_link):
        page_select = driver.find_element(by=By.XPATH, value = '/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[103]/td')
        elements = driver.find_elements(by=By.CLASS_NAME, value = 'a')
        for element in elements:
            if (element.text == str(i)):
                element.click()

def open_all(driver: webdriver) -> str:
    table = driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[2]/tbody')
    for element in table.find_elements(by = By.TAG_NAME, value = "tr"):
        children = element.find_elements(by=By.TAG_NAME, value = 'td')
        if (len(children) == 1):
            continue

        child = element.find_element(by=By.CLASS_NAME, value = "width")
        to_click = child.find_element(by=By.TAG_NAME, value = 'a')
        to_click.click()
    
    return driver.page_source
    


main_url = "https://catalog.rpi.edu/index.php"
driver = webdriver.Firefox()
driver.implicitly_wait(2)
link = get_course_link(driver, 1)

#open_all(driver, link)
get_all_html(driver, link)

#driver.close()
