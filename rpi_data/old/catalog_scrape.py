from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import lxml
from lxml import etree

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
    page_sources = []
    page_sources.append(open_all(driver))
    time.sleep(5)
    for i in range(2, maximum_link + 1):
        table = driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[2]/tbody')
        page_select = table.find_elements(by=By.TAG_NAME, value = 'tr')[-1]
        elements = page_select.find_elements(by=By.TAG_NAME, value = 'a')
        for element in elements:
            if (element.text == str(i)):
                element.click()
                time.sleep(5)
                break
        page_sources.append(open_all(driver))
    return page_sources

def open_all(driver: webdriver) -> str:
    table = driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[2]/tbody')
    for element in table.find_elements(by = By.TAG_NAME, value = "tr"):
        children = element.find_elements(by=By.TAG_NAME, value = 'td')
        if (len(children) == 1):
            continue

        child = element.find_element(by=By.CLASS_NAME, value = "width")
        to_click = child.find_element(by=By.TAG_NAME, value = 'a')
        to_click.click()
    
    time.sleep(5)
    return driver.page_source
    
def soup_all(page_sources: list[str]) -> dict[str, dict[str, str]]:
    for source in page_sources:
        soup_one(source)

def soup_one(page_source: str):
    tree = etree.HTML(page_source)
    table = tree.xpath("/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[2]/tbody")[0]
    tr_tags = table.getchildren()
    for tag in tr_tags:
        if (len(tag.getchildren()) == 1):
            continue
        td = tag.getchildren()[1]
        inner_table = td.findall('table')
        course_padding = inner_table[0].getchildren()[0].getchildren()[0].getchildren()[0]
        info = course_padding.findall('div')[1]
        title = info.findall('h3')[0].text
        print(title)
        description = etree.tostring(info.find('hr'), encoding='unicode').replace("<hr/>", "")
        data_to_split = etree.tostring(info, encoding = 'unicode')
        split_by_bold = data_to_split.split("<strong>")
        split_by_bold.pop(0)
        parts = dict()
        for each in split_by_bold:
            part_title = each.split("</strong>")[0]
            parts[part_title] = dict()
            #print(each.split("</strong>")[1])
            temp_tree = etree.HTML(each.split("</strong>")[1])
            inner = temp_tree.find('body')
            links = inner.findall('a')
            #print(etree.tostring(inner, encoding = 'unicode'))
            text = ""
            queue = [inner]
            while (len(queue) > 0):
                checking = queue.pop()
                print(etree.tostring(checking))
                if (checking.text != None and checking.text != "Close"):
                    text += checking.text
                [queue.append(i) for i in checking.getchildren()]
            print(text)
            #if len(links) > 0:
                #print(links[0].text)
            
            
        #print(description)
            



main_url = "https://catalog.rpi.edu/index.php"
driver = webdriver.Firefox()
driver.implicitly_wait(2)
link = get_course_link(driver, 1)

source = open_all(driver)
soup_one(source)

#sources = get_all_html(driver, link)
#soup_all(sources)

#driver.close()
