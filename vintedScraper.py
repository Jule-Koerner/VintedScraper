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



"""Scrapes "Vinted" and downloads all images that match the user input.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""



class VintedScraper:
    """Scrapes "Vinted" and downloads all images that match the user's input.


    """
    def __init__(self, url, pages):
        self.current_url = url
        self.current_page = 1
        self.driver = webdriver.Firefox()
        self.pages = pages

    def get_next_page(self):

        self.current_url = self.current_url.replace(f"&page={self.current_page}", f"&page={self.current_page + 1}")
        self.current_page += 1
        self.driver.get(self.current_url)
        print(self.current_url)

    def download_image(self, img_ref: str, file_name: str) -> str:

        image_content = requests.get(img_ref).content  # gives image
        image_file = io.BytesIO(image_content)  # convert into byteio datatype (store file im memory)
        # convert to image
        image = Image.open(image_file)
        file_path = r"C:\Users\jule-\Documents\Uni\SciPy\vintedScraper\scraped_imgs" + file_name
        with open(file_path, "wb") as f:
            image.save(f, "png")
        print("SUCCESS")
        return file_path

    def scrape_page(self):
        final_paths = []
        final_urls = []

        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        target_parents = list(soup.find_all("div", {"class": "ItemBox_image__3BPYe"}))

        try:

            for i, p in enumerate(target_parents):

                print("NEW ELEMENT _------------------------------------------------------")
                # print(p)

                href = p.find("a", href=True)["href"]
                print("href", href)
                image_srcs = p.find("img")["src"]

                image_path = self.download_image(image_srcs, f"\{i}img.png")

                print("image path", image_path)
                final_paths.append(image_path)
                final_urls.append(href)

            return tuple(final_urls, final_paths)

        except Exception as e:
            print(e)
            print("TYPE", type(href))

        #links = soup.find_all('a', {"class": "ItemBox_overlay__1kNfX"}, href=True)





        # Only append if filters match user preferences
        # for i, link in enumerate(links):
        #     self.driver.get(link["href"])
        #     img_html = self.driver.page_source
        #     img_soup = BeautifulSoup(img_html, "html.parser")
        #
        #     target_image = img_soup.find('a', {"class": "item-thumbnail is-loaded"}, href=True)
        #     print("target image", target_image)
        #     target_image_ref = target_image["href"]
        #
        #     print("target_image_ref", target_image_ref)
        #
        #     image_path = self.download_image(target_image_ref, f"\{i}img.png")
        #     final_paths.append(image_path)
        #     final_urls.append(target_image_ref)

        return (final_urls, final_paths)

    def __call__(self):
        print("current url", self.current_url)

        self.driver.get(self.current_url)  # opens page
        final_paths = []
        final_urls = []

        # this is just to ensure that the page is loaded
        time.sleep(2)
        urls, paths = self.scrape_page()
        if len(paths) != 0:
            final_paths.append(paths)
            final_urls.append(urls)

        print("FINAL URLS", final_urls)
        print("FINAL PATHS", final_paths)

        if self.pages != 1:
            for _ in range(self.pages):
                print("new page current url", self.current_url)
                print("Next page")

                self.get_next_page()
                urls, paths = self.scrape_page()

                if len(paths) != 0:
                    final_paths.append(paths)
                    final_urls.append(urls)

        final_paths = list(itertools.chain(*final_paths))
        final_urls = list(itertools.chain(*final_urls))



        return final_paths, final_urls



