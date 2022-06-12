#### This program scrapes naukri.com's page and gives our result as a
#### list of all the job_profiles which are currently present there.
import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import itertools
import numpy as np
 #Male/femal/child


def get_url(input):

    if input == "damen":
        return "https://www.vinted.de/damen"

    if input == "herren":
        return "https://www.vinted.de/herren"

    if input == "kinder":
        return "https://www.vinted.de/kinder"


def getNextPage(driver):
    #Geet next page

    elem = driver.find_element(By.CLASS_NAME,"Pagination_next__DUhdH")

    driver.execute_script("arguments[0].click()", elem)

    # #Make sure that page exists before accessing information
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


def scrape_page(driver, size: str, price: float):
    hrefs = []

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all('a', {"class": "ItemBox_overlay__1kNfX" } , href = True)


    #Only append if filters match user preferences
    for link in links:

        elem = link["title"]
        size_match = size_filter(elem, size)
        price_match = price_filter(elem, price)

        if size_match and price_match:
            hrefs.append(link["href"])

    return hrefs




def scrape_vinted(person= "damen", size="M", price=50, pages=30):
    final_elements = []
    url = get_url(person)

    driver = webdriver.Firefox()
    driver.get(url)  # opens page

    # this is just to ensure that the page is loaded
    time.sleep(5)

    page = scrape_page(driver, size, price)
    if len(page) != 0:
        final_elements.append(page)

    for _ in range(pages):
        getNextPage(driver)
        page = scrape_page(driver, size, price)
        if len(page) != 0:
            final_elements.append(page)


    final_elements = list(itertools.chain(*final_elements))
    print(final_elements[0])







scrape_vinted()

