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
        """
        Constructor for the WorldFlagScrapper class which creates a new instance of scrapper object
        Initialize instance variables
        :param url: The url of the website to scrap
        """

        self.url = url  # Url of website to scrap
        self.soup = None  # Holds the scrapped soup
        self.flags_div = None  # Holds the scrapped page flags container
        self.countries_data = {}  # Raw data dictionary
        self.site_url = "https://www.worldometers.info"  # Url of the site, which is needed for getting correct img location
        self.img_folder = "flags_images"  # Folder to hold the scrapped flag images
        self.json_file = "flags_data.json"  # JSON database to store country name and relative path of images
        self.json_data_dict = {}  # Dictionary to hold data before it's dumped to JSON database
        self.scrap_record_json = "scrap_record.json"  # Raw JSON data

    # get the url page
    def url_connection(self):
        """
        Method to connect to the website
        Set the self.soup to the scrapped page soup
        :return: None
        """
        try:
            # Send a request and create a soup using BeautifulSoup
            response = requests.get(self.url)
            parse_page = BeautifulSoup(response.text, "html.parser")

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
        """
        Method to scrap specific flags container from the soup
        Set self.flags_div to scrapped soup
        :return: None
        """
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
        """
        Method to get the countries name and flags url from the soup
        Add the raw data into self.countries_data
        :return: None
        """
        if self.flags_div:
            try:
                flag_items = self.flags_div.find_all("div", class_="col-md-4") # Find all div with that class
                for flag in flag_items: # Loop through each items in flag_items
                    country_outer_div = flag.find(attrs={"style": "margin-top:10px "})

                    if country_outer_div: # If country_outer_div exist
                        # Find the inner div which contains country name and img tag
                        country_inner_div = country_outer_div.find(
                            attrs={"style": "font-weight:bold; padding-top:10px"})
                        country_flag_url_holder = country_outer_div.find("img")

                        if country_inner_div and country_flag_url_holder: # If both exists
                            # Get the country name and img source
                            country_name = country_inner_div.text
                            country_flag_url = country_flag_url_holder.get("src")

                            if country_name and country_flag_url: # If both country name and flag url exist
                                # Modify the img source to remove small tag so larger size img can be downloaded
                                update_img_url = country_flag_url.replace("/small/tn_", "/")
                                # Add the raw data into countries data dictionary
                                self.countries_data[country_name] = {
                                    "name": country_name,
                                    "flag_img_url": update_img_url,
                                    "flag_web_address": self.site_url + update_img_url,
                                }
                            # Bunch of error checking messages
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
        """
        Method to create an image folder if one is not already created
        :return: None
        """
        try:
            if not os.path.exists(self.img_folder):
                os.makedirs(self.img_folder)
                print(f"Image folder created successfully as {self.img_folder}")
        except OSError as e:
            print(f"Sorry there was an OS error: {e}")

    # download the image
    def download_flags(self):
        """
        Method to download the flags from the scrapped page
        :return: None
        """
        if self.countries_data: # If data exist in countries data
            for country, data in self.countries_data.items(): # Loop through dictionary
                flag_url = data["flag_web_address"] # Get the modified image source from the dictionary
                response = requests.get(flag_url) # Send a request to the website

                if response.status_code == 200: # If there was no problem
                    # Create a name for each image using string concatenation of country name plus img source
                    img_name = f"{country}_flag.gif"
                    img_path = os.path.join(self.img_folder, img_name)

                    # save to folder
                    try:
                        # Open the image folder and save the images
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
        """
        Method to create JSON database using scrapped data of countries name and relative image address
        :return: None
        """
        try:
            with open(self.json_file, "w", encoding="utf=8") as json_file:
                json.dump(self.json_data_dict, json_file, indent=4)
                print(f"Written to JSON File {self.json_file}")

            with open(self.scrap_record_json, "w", encoding="utf=8") as scrap_json_record:
                json.dump(self.countries_data, scrap_json_record, indent=4)
                print(f"Written to JSON File {self.scrap_record_json}")
        except Exception as e:
            print(f"Data did not write to json file: {e}")
