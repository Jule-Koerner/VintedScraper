#### This program scrapes naukri.com's page and gives our result as a
#### list of all the job_profiles which are currently present there.
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
 #Male/femal/child



url = "https://www.vinted.de/damen"



driver = webdriver.Chrome(r'C:\Users\jule-\Downloads\chromedriver_win32\chromedriver.exe')
driver.get(url)

# this is just to ensure that the page is loaded
time.sleep(5)


def getNextPage():
    #Geet next page
    elem = driver.find_element(By.CLASS_NAME,"Pagination_next__DUhdH")
    elem.click()

    #Make sure that page exists before accessing information
    # try:
    #     element = WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.ID, "myDynamicElement"))
    #     )
    # finally:
    #     driver.quit()

def price_filter(elem, max_price: float):

    after_key = re.findall(r"(?<=Preis:).*", elem)[0]
    split_string = after_key.split()
    price = float(split_string[0].replace(",", "."))

    if price > max_price:
        return False
    else:
        return True


def size_filter(elem, target_size: str):
    after_key = re.findall(r"(?<=Größe:).*", elem)[0]
    split_string = after_key.split()
    print(split_string)

    size_dict = {"Xs":["Xs", "xs", 32, 34],
                 "S": ["S","s", 36, 38],
                 "M": ["M", "m", 40, 42],
                 "L": ["L", "l", 44, 46],
                 "XL": ["XL", "xl", 48, 50],
                 "XXL": ["XXL", "xxl", 52, 54]
                 }
    try:
        size_dict[target_size]
    except:
        return False

    else:
        if len(list(set(split_string) & set(size_dict[target_size])))!=0:
            return True
        else:
            return False


def scrape_page():
    hrefs = []
    links = driver.find_elements(By.XPATH, "//a[@class = 'ItemBox_overlay__1kNfX'][@href]")
    print("Lämnge", len(links))

    #Only append if filters match
    for link in links:
        elem = link.get_attribute("title")
        size_match = size_filter(elem, "M")
        price_match = price_filter(elem, float(40))

        if size_match and price_match:
            hrefs.append(link.get_attribute("href"))


    return hrefs




scrape_page()





