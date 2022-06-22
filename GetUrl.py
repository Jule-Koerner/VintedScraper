import numpy as np

class GetUrl:

    def __init__(self, gender= "damen", women_size = "M", men_size= "L", price=30, bh_size = "A", colors= ["rot", "rose"]):

        self.gender = gender
        self.price = price
        self.colors = colors
        self.women_size = women_size
        self.men_size = men_size
        self.bh_size = bh_size

        self.current_page = 1
        self.current_url = None

    def get_gender_id(self):

        gender_mapping = {
            "damen": 1904,
            "herren": 5,
        }

        gender_string = ""

        if len(self.gender)!=0:

            for g in self.gender:
                gender_string = gender_string+f"&catalog[]={gender_mapping[g]}"

            return gender_string
        else:
            return None


    def get_color_id(self):
        color_mapping = {
            "rot": 7,
            "rose": 24,
            "burgunderrot": 23,
            "grün": 10,
            "dunkelgrün": 28,
            "khaki": 16,
            "braun": 2,
            "blau": 9,
            "senffarben": 29,
            "gelb": 8,
            "orange": 11,
            "schwarz": 1,
            "weiß": 12,
            "creme": 20,
            "aprikose": 21,
            "beige": 4,
            "korallenrot": 22,
            "bunt": 15,
            "pink": 5,
            "lila": 6,
            "flieder": 25,
            "hellblau": 26,
            "grau": 3,
            "silber": 13,
            "gold": 14,
            "marineblau": 27,
            "türkis": 17,
            "mintgrün": 30
        }

        final_string = ""
        if len(self.colors != 0):
            for color in self.colors:
                final_string = final_string+f"&color_id[]={color_mapping[color]}"

            return final_string
        else:
            return None

    def get_price_id(self):
        if self.price!=None:

            return f"&price_to{self.price}"
        else:
            return None

    def get_women_size_id(self):
        women_clothing_size_mapping: dict = {"XXXS": 1226, "XXS": 102, "XS": 2,
                                     "S": 3,
                                     "M": 4,
                                     "L": 5,
                                     "XL": 6, "XXL": 7, "XXXL": 310, "4XL": 311, "5XL": 312, "6XL": 1227, "7XL": 1228, "8XL": 1229,"9XL": 1230}
        final_string = ""
        if len(self.women_size) != 0:
            for size in self.women_size:
                final_string = final_string+f"&size_id[]={women_clothing_size_mapping[size]}"
            return final_string

        else:
            return None


    
    def get_men_size_id(self):
        men_size_clothing_mapping: dict = {key: value for key, value in
                                   zip(["XS",
                                        "S",
                                        "M",
                                        "L",
                                        "XL", "XXL", "XXXL"],
                                       range(206, 213))}

        final_string = ""
        if len(self.men_size) != 0:
            for size in self.men_size:
                final_string = final_string + f"&size_id[]={men_size_clothing_mapping[size]}"
            return final_string
        else:
            return None


    def get_bh_size_id(self):

        women_size_bh_id: dict = {str(key) + key_addition: key + 1182 + counter for key in
                               (65, 100, 5) for counter, key_addition in enumerate(
                ["A&AA", "B", "C", "D", "E", "F", "G", "H", "J"])}
        final_string = ""
        if len(self.bh_size)!=0:
            for size in self.bh_size:
                final_string = final_string + f"&size_id[]={women_size_bh_id[size]}"

            return final_string
        else:
            return None



    def get_url(self):
        color = self.get_color_id()
        gender = self.get_gender_id()
        women_size = self.get_women_size_id()
        men_size = self.get_men_size_id()
        bh_size = self.get_bh_size_id()
        price = self.get_price_id()
        base_url = "https://www.vinted.de/vetements?currency=EUR"

        if gender != None:
            base_url+gender
        if color != None:
            base_url+color
        if price != None:
            base_url+price

        if women_size != None:
            base_url+women_size

        if men_size != None:
            base_url + men_size

        if bh_size != None:
            base_url + bh_size

        self.current_url = base_url

    def get_next_url(self):

        self.current_url = self.current_url.replace(f"&page= {self.current_page}", f"&page= {self.current_page + 1 }")
        self.current_page += 1

        return self.current_url









men_size_shoes: dict = {key: value for key, value in
                        zip(range(38, 47), range(776, 794, 2))}


women_size_shoes: dict = {key: key + 20 for key in range(35, 43)}







test = GetUrl()
test.get_color_id()