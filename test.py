import io
import re
from io import BytesIO
from PIL import Image

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

import ImageSimilarity
import matplotlib.pyplot as plt
import kNearestClothes
import GetUrl


def download_image(img_ref, file_name="img.png"):
    # <figure class=><a rel="fancybox" class="item-thumbnail is-loaded" href="https://images1.vinted.net/t/02_01621_ga78eZMJ98aubfFPiSBEV1Cf/f800/1654847746.jpeg?s=41e0fe38d7fd7c4f715908414024656b01b224d9"><img alt="Vinted    Ladies floral dress" title="Vinted    Ladies floral dress" width="624" height="624" class="item-thumbnail lazy-thumbnail __act_as_lazy loaded" data-src="https://images1.vinted.net/t/02_01621_ga78eZMJ98aubfFPiSBEV1Cf/f800/1654847746.jpeg?s=41e0fe38d7fd7c4f715908414024656b01b224d9" data-item-id="1952035299" data-item-owner-id="96118930" data-disable-tracking="true" data-lazyload-background="true" itemprop="image" style="background-image: url(https://images1.vinted.net/t/02_01621_ga78eZMJ98aubfFPiSBEV1Cf/f800/1654847746.jpeg?s=41e0fe38d7fd7c4f715908414024656b01b224d9);" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"></a></figure>
    # parent = img_soup.find("figure", {"class": "item-description item-photo item-photo--1"})
    # child = parent.contents[0]
    # ref = child["href"]
    #
    image_content = requests.get(img_ref).content  # gives image
    image_file = io.BytesIO(image_content)  # convert into byteio datatype (store file im memory)
    # convert to image
    image = Image.open(image_file)
    file_path = r"C:\Users\jule-\Documents\Uni\SciPy\vintedScraper\scraped_imgs" + file_name
    with open(file_path, "wb") as f:
        image.save(f, "png")
    print("SUCCESS")
    return file_path


# def get_url(input):
#     if input == "damen":
#         return "https://www.vinted.de/vetements?catalog[]=5&color_id[]=3&price_to=30&currency=EUR&size_id[]=207"
#
#     if input == "herren":
#         return "https://www.vinted.de/herren"
#
#     if input == "kinder":
#         return "https://www.vinted.de/kinder"

#
# def getNextPage(driver):
#     # Geet next page
#     elem = driver.find_element(By.CLASS_NAME, "Pagination_next__DUhdH")
#
#     driver.execute_script("arguments[0].click()", elem)

    # #Make sure that page exists before accessing information
    # try:
    #     element = WebDriverWait(driver, 20).until(
    #         EC.presence_of_element_located((By.ID, "myDynamicElement"))
    #     )
    # finally:
    #     driver.quit()


# def price_filter(elem, max_price: float):
#     after_key = re.findall(r"(?<=Preis:).*", elem)[0]
#     split_string = after_key.split()
#     price = float(split_string[0].replace(",", "."))
#
#     if price > max_price:
#         return False
#     else:
#         return True


# def size_filter(elem, target_size: str):
#     after_key = re.findall(r"(?<=Größe:).*", elem)[0]
#     split_string = after_key.split()
#
#     size_dict = {"Xs": ["Xs", "xs", 32, 34],
#                  "S": ["S", "s", 36, 38],
#                  "M": ["M", "m", 40, 42],
#                  "L": ["L", "l", 44, 46],
#                  "XL": ["XL", "xl", 48, 50],
#                  "XXL": ["XXL", "xxl", 52, 54]
#                  }
#     try:
#         size_dict[target_size]
#     except:
#         return False
#
#     else:
#         if len(list(set(split_string) & set(size_dict[target_size]))) != 0:
#             return True
#         else:
#             return False

#
# def get_color(img_soup):
#     color = img_soup.find(itemprop="color").contents
#
#     print("color", color)
#     print("type list", type(color))
#     print("first elem", type(color[0]))
#
#     if "," in color[0]:
#         print("im in")
#         color = color[0].split(", ")
#         print("color after split", color)
#         print("type",type(color))
#
#     return color


def scrape_page(driver):

    final_paths = []
    final_urls = []

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all('a', {"class": "ItemBox_overlay__1kNfX"}, href=True)

    # Only append if filters match user preferences
    for i, link in enumerate(links):

        driver.get(link["href"])
        img_html = driver.page_source
        img_soup = BeautifulSoup(img_html, "html.parser")

        target_image = img_soup.find('a', {"class": "item-thumbnail is-loaded"}, href=True)
        target_image_ref = target_image["href"]

        image_path = download_image(target_image_ref, f"{i}img.png")
        final_paths.append(image_path)
        final_urls.append(target_image_ref)


    return (final_urls, final_paths)



        #elem = link["title"]
        #size_match = size_filter(elem, size)
        #price_match = price_filter(elem, price)

        # if size_match and price_match:
        #     #ToDO
        #     # only Beautiful soup
        #     current_page = driver.get(link["href"])
        #     img_html = driver.page_source
        #     img_soup = BeautifulSoup(img_html, "html.parser")
        #
        #     color = get_color(img_soup)
        #     # color = img_soup.find(itemprop = "color").contents
        #
        #     image_path = download_image(img_soup, file_name=f"\img{i}.png")
        #     final_element = (image_path, list(color))
        #     final_elements.append(final_element)
        #     final_refs.append(link["href"])



def scrape_vinted(gender, size, price, pages, colors):
    final_paths = []
    final_urls = []

    url = GetUrl.GetUrl(gender, size, price, colors)
    current_url = url.get_url()


    driver = webdriver.Firefox()
    driver.get(current_url)  # opens page

    # this is just to ensure that the page is loaded
    time.sleep(2)

    urls, paths = scrape_page(driver)
    if len(pages) != 0:
        final_paths.append(paths)
        final_urls.append(urls)

    for _ in range(pages):

        current_url = url.get_next_url()
        driver.get(current_url)

        if len(pages) != 0:
            final_paths.append(urls)

            final_urls.append(paths)

    # for _ in range(pages):
    #     driver.get(url)
    #     getNextPage(driver)
    #     urls, paths = scrape_page(driver)
    #     if len(pages) != 0:
    #         final_paths.append(urls)
    #
    #         final_urls.append(paths)



    scraped_images_with_color_tag = list(itertools.chain(*final_paths))

    vectors = ImageSimilarity.AllSimilarityVectors(scraped_images_with_color_tag)
    distances = vectors() #all similarity vectors

    targets = kNearestClothes.k_nearest_neighbors(distances, len(distances)) #gives indices for 10 nearest neighbors

    to_plot = []
    dist_to_plot = []

    for i in range(len(distances)):
        to_plot.append(scraped_images_with_color_tag[targets[0][i]])
        dist_to_plot.append(list(distances[targets[0][i]]))



    kNearestClothes.plot_k_nearest_neighbors(np.array(dist_to_plot), np.array(to_plot), 'scraped_imgs/img0.png')




    print(targets)




scrape_vinted()
