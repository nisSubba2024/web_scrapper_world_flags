"""
 * //////////////////////////////////////////////////////////////////////
 *      PROGRAM: WORLD_FLAGS/FLAG_SCRAPPER.PY
 *      Written by Nishan Subba
 *      GitHub: @nisSubba2024
 *      Purpose: Web scrapper for world flags
 *      Last Date Modified: Dec 31, 2024
 * //////////////////////////////////////////////////////////////////////
"""
import json
import os

import requests
from bs4 import BeautifulSoup


class WorldFlagScrapper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.flags_div = None
        self.countries_data = {}
        self.site_url = "https://www.worldometers.info"
        self.img_folder = "flags_images"
        self.json_file = "flags_data.json"
        self.json_data_dict = {}
        self.scrap_record_json = "scrap_record.json"

    # get the url page
    def url_connection(self):
        try:
            response = requests.get(self.url)
            parse_page = BeautifulSoup(response.text, "html.parser")
            # print(parse_page.prettify())
            if parse_page:
                print("Page successfully parsed")
            self.soup = parse_page
        except requests.exceptions.HTTPError as e:
            print(f"Sorry there was an HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Sorry there was an Connection Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Sorry there was an error with your request: {e}")

    # get the specific section about flags
    def flags_wrapper(self):
        if self.soup:
            try:
                flags_container_div = self.soup.find(attrs={"style": "width:95%; text-align:left"})
                self.flags_div = flags_container_div
            except requests.exceptions.HTTPError as e:
                print(f"Sorry there was an HTTP Error: {e}")
            except requests.exceptions.ConnectionError as e:
                print(f"Sorry there was an Connection Error: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Sorry there was an error with your request: {e}")
        else:
            print("No soup found")

    # scrap flags from flag container
    def scrap_flags(self):
        if self.flags_div:
            try:
                flag_items = self.flags_div.find_all("div", class_="col-md-4")
                for flag in flag_items:
                    country_outer_div = flag.find(attrs={"style": "margin-top:10px "})
                    if country_outer_div:
                        country_inner_div = country_outer_div.find(
                            attrs={"style": "font-weight:bold; padding-top:10px"})
                        country_flag_url_holder = country_outer_div.find("img")
                        if country_inner_div and country_flag_url_holder:
                            country_name = country_inner_div.text
                            country_flag_url = country_flag_url_holder.get("src")
                            if country_name and country_flag_url:
                                # print(f"{country_name}: {country_flag_url}")
                                update_img_url = country_flag_url.replace("/small/tn_", "/")
                                self.countries_data[country_name] = {
                                    "name": country_name,
                                    "flag_img_url": update_img_url,
                                    "flag_web_address": self.site_url + update_img_url,
                                }
                            else:
                                print("No country name and flag url found")
                        else:
                            print("No country inner div found")
                    else:
                        print("No country outer div found")
            except requests.exceptions.RequestException as e:
                print(f"Sorry there was an error with your request: {e}")
        else:
            print("Flag DIV did not get scrapped")

    # create a folder
    def create_image_folder(self):
        try:
            if not os.path.exists(self.img_folder):
                os.makedirs(self.img_folder)
                print(f"Image folder created successfully as {self.img_folder}")
        except OSError as e:
            print(f"Sorry there was an OS error: {e}")

    # download the image
    def download_flags(self):
        if self.countries_data:
            for country, data in self.countries_data.items():
                flag_url = data["flag_web_address"]
                response = requests.get(flag_url)
                if response.status_code == 200:
                    img_name = f"{country}_flag.gif"
                    img_path = os.path.join(self.img_folder, img_name)

                    # save to folder
                    try:
                        with open(img_path, "wb") as img_folder:
                            img_folder.write(response.content)
                            self.json_data_dict[country] = {
                                "name": data["name"],
                                "flag_src": self.img_folder + "/" + img_name
                            }
                        print(f"Image for {data["name"]} successfully downloaded as {img_name} ")
                    except Exception as e:
                        print(f"Image did not downloaded to folder: {e}")
                else:
                    print(f"Failed to download image for {data['name']}. Status code: {response.status_code}")
        else:
            print("No countries data found")

    # insert data into json file
    def create_json_database(self):
        try:
            with open(self.json_file, "w", encoding="utf=8") as json_file:
                json.dump(self.json_data_dict, json_file, indent=4)
                print(f"Written to JSON File {self.json_file}")

            with open(self.scrap_record_json, "w", encoding="utf=8") as scrap_json_record:
                json.dump(self.countries_data, scrap_json_record, indent=4)
                print(f"Written to JSON File {self.scrap_record_json}")
        except Exception as e:
            print(f"Data did not write to json file: {e}")
