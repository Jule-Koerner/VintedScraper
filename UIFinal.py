import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
from tkinter import *

import kNearestClothes
import vintedScraper
import NetworkSimilarity

men_size_clothing: dict = {key: value for key, value in
                           zip(["XS", "S", "M", "L", "XL", "XXL", "XXXL"],
                               range(206, 211))}
men_size_shoes: dict = {str(key): value for key, value in
                        zip(range(38, 47), range(776, 794, 2))}

women_size_clothing: dict = {"XXXS": 1226, "XXS": 102, "XS": 2, "S": 3, "M": 4,
                             "L": 5, "XL": 6, "XXL": 7, "XXXL": 310, "4XL": 311,
                             "5XL": 312, "6XL": 1227, "7XL": 1228, "8XL": 1229,
                             "9XL": 1230, }
women_size_shoes: dict = {str(key): key + 20 for key in range(35, 43)}
women_size_bh: dict = {str(key) + key_addition: key + 1182 + counter for key in
                       (65, 100, 5) for counter, key_addition in enumerate(
        ["A&AA", "B", "C", "D", "E", "F", "G", "H", "J"])}


women_category: dict = {"Mäntel & Jacken": 1037, "Hoodies & Pullover": 13, "Blazer & Anzüge": 8, "Kleider": 10,
                        "Röcke": 11, "Tops & T-shirts": 12, "Jeans": 183, "Hosen & Leggins": 9, "Shorts": 15,
                        "Jumpsuit": 1035, "Bademode": 28, "Unterwäsche & Nachtwäsche": 29, "Activewear": 74
                        }
men_category: dict = {"Jeans": 257, "Jacken & Mäntel": 1206, "Tops & Tshirts": 76, "Anzug & Blazer": 32,
                        "Pullover & Sweater": 79, "Hosen": 34, "Shorts": 80, "Unterwäsche & Socken": 85,
                        "Sportartikel": 30}


link: str = "https://www.vinted.de/vetements?currency=EUR"
root = tk.Tk()

# config the root window
root.geometry('500x500')
root.config(background = "black")
root.resizable(False, False)
root.title('Combobox Widget')

image_path: str = ""
class DropdownAttribute:
    """Class for picking a certain attribute"""

    def __init__(self, attribute_dict: dict, label: str, attribute_start: str = "&size_id[]=") -> object:
        # label
        label = Label(text=label, fg = "white", bg="black")
        label.pack(fill=tk.X, side=tk.TOP)
        # create a combobox
        self.text = tk.StringVar()
        attribute_cb = ttk.Combobox(root, textvariable=self.text)
        self.attribute_dict: dict = attribute_dict
        # get first 3 letters of every month name
        attribute_cb['values'] = list(attribute_dict.keys())

        # prevent typing a value
        attribute_cb['state'] = 'readonly'

        # place the widget
        attribute_cb.pack(fill=tk.X, side=tk.TOP)

        attribute_cb.bind('<<ComboboxSelected>>', self.attribute_changed)

        # set the current month
        self.current_value = ""
        self.attribute_start = attribute_start
        attribute_cb.set(self.current_value)

    # bind the selected value changes
    def attribute_changed(self, event):
        """ handle the month changed event """
        # showinfo(
        #     title='Result',
        #     message=f'The string addtion is: {self.attribute_dict[self.text.get()]}!'
        # )
        self.current_value = self.attribute_dict[self.text.get()]
        global link
        link += self.attribute_start + str(self.current_value)


# Create a File Explorer label
label_file_explorer = Label(root,
                            text="Choose a file",
                            fg="white", bg="black")
label_file_explorer.pack(fill=tk.X, side=tk.TOP)
# Function for opening the
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("PNG files",
                                                      "*.png*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="Chosen File: " + filename)
    print("filename", filename)
    image_path = filename
    print("image path", image_path)


button_explore = Button(root,
                        text="Browse Files",
                        command=browseFiles)

button_explore.pack(fill=tk.X, side = tk.TOP)

men_size_clothing_dd = DropdownAttribute(men_size_clothing, "Clothing size (men): ")
women_size_clothing_dd = DropdownAttribute(women_size_clothing, "Clothing size (women): ")

men_size_shoes_dd = DropdownAttribute(men_size_shoes, "Shoe size (men): ")
women_size_shoes_dd = DropdownAttribute(women_size_shoes, "Shoe size (women): ")

women_size_bh_dd = DropdownAttribute(women_size_bh, "BH size: ")

women_category_dd = DropdownAttribute(women_category, "Which category matches your input image the most (women)?: ", "&catalog[]=")

men_category_dd = DropdownAttribute(men_category, "Which category matches your input image the most (men)?: ", "&catalog[]=" )

def get_matches():
    print("Hello")
    print("query image path", image_path)
    print(type(link))
    final_link = link+"&page=1"
    print("type final link", final_link)
    print("start link", final_link)
    scraper = vintedScraper.VintedScraper(final_link, pages=50)

    #Start scraping

    paths, urls = scraper()

    print("final urls", urls)
    print("final paths", paths)


    network_similarity = NetworkSimilarity.NetworkSimilarity(r"C:\Users\jule-\Documents\Uni\SciPy\vintedScraper\images\karo.png", paths)
    cosine_similarity = network_similarity.cosine_similarities()
    print(cosine_similarity)

    knearest = kNearestClothes.KNearestClothes(cosine_similarity)
    knearest()
    knearest.plot_k_nearest_clothes(paths, r"C:\Users\jule-\Documents\Uni\SciPy\vintedScraper\images\karo.png")




print("imga", image_path)

button_explore = Button(root,
                        text="Start searching",
                        command=get_matches)

button_explore.pack(fill=tk.X, side = tk.TOP)

while True:

    root.update_idletasks()
    root.update()
