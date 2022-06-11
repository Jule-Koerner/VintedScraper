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

def scrapePage():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser") #besser driver.page_source
    html_source = driver.page_source

    links = soup.find_all('a', {"class": "ItemBox_overlay__1kNfX" } , href = True)

    links =[link["href"] for link in links]



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

def priceFilter(elem):
    #filter Price
    #test_string = links[10].get_attribute("title")
    print(test_string)
    #split_string = np.array(links[0].get_attribute("title").split("Preis:"))
    after_key = re.findall(r"(?<=Preis:).*", elem)[0]
    split_string = after_key.split()
    price = float(split_string[0].replace(",", "."))

    #return true or false


def sizeFilter(elem):
    after_key = re.findall(r"(?<=Größe:).*", elem)[0]
    split_string = after_key.split()
    print(split_string)

    pass
#Return true or false





def selScrapePage():
    hrefs = []

    links = driver.find_elements(By.XPATH, "//a[@class = 'ItemBox_overlay__1kNfX'][@href]")

    #filter Price
    test_string = links[19].get_attribute("title")

    print(test_string)
    #split_string = np.array(links[0].get_attribute("title").split("Preis:"))
    after_key = re.findall(r"(?<=Preis:).*", test_string)[0]
    split_string = after_key.split()
    price = float(split_string[0].replace(",", "."))



    #filter size
    after_key = re.findall(r"(?<=Größe:).*", test_string)[0]
    split_string = after_key.split()
    print(split_string)

    #Only append if filters pass
    # for link in links:
    #     elem = link.get_attribute("title")
    #     sizeMatch = sizeFilter(elem)
    #     priceMatch = priceFilter(elem)
    #
    #     if sizeMatch and priceMatch:
    #         hrefs.append(links)
    #
    # return hrefs







    #print(split_string)
    #target_index = int(np.where(split_string == "Preis:"))
    #print(target_index)
    #price = float(split_string[target_index[0]+1][0])
    #print("preis", price)







selScrapePage()





