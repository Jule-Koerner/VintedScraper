#### This program scrapes naukri.com's page and gives our result as a
#### list of all the job_profiles which are currently present there.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
 #Male/femal/child

def selectUrl(input):
    if input == "damen":
        return "https://www.vinted.de/damen"

    if input == "herren":
        return "https://www.vinted.de/herren"

    if input == "kinder":
        return "https://www.vinted.de/kinder"


# # url of the page we want to scrape
url = selectUrl("damen")

def makeSoup(url):
    # initiating the webdriver
    driver = webdriver.Chrome(r'C:\Users\jule-\Downloads\chromedriver_win32\chromedriver.exe')
    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup


def scrapePage(soup):

    links = soup.find_all('a', {"class": "ItemBox_overlay__1kNfX" } , href = True)
    links =[link["href"] for link in links]
    return links




#links = list(filter(lambda link: link["href"], links))


#propagate through pages
def loopPages(url):
    soup = makeSoup(url)
    hrefs = []
    hrefs.append(scrapePage())

    #get next page
    next_page = soup.find("a", {"class": "Pagination_next_DUhdH"}, href = True)
    if loops <=50:

        loopPages(next_page, loops++)
    return

def wrapper():
    currentUrl = selectUrl("damen")
    currentSoup = makeSoup(currentUrl)
    images = scrapePage(currentSoup)


#main
page = loopPages(selectUrl("damen"))
