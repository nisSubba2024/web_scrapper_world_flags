# World Flags Web Scraper

This program scrapes all the world flags from [Worldometers Flags of the World](https://www.worldometers.info/geography/flags-of-the-world/) and stores the flag image URLs and other related data.

## Features

- Scrapes flag images and country names.
- Downloads flag images and stores them in a local folder.
- Saves scraped data in a JSON file.
- Optionally saves metadata of downloaded flags in a separate JSON file.

## Requirements

- Python 3.x
- `requests` library
- `BeautifulSoup` from `bs4`
- `json`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/nisSubba2024/world-flags-scraper.git
   ```

2. Install the necessary Python libraries
    ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the following script
    ```bash
   python3 main.py
    ```
2. The program will:
    - Connect to the Worldometers flags page.
    - Scrape country names and flag URLs.
    - Download the flags and save them in the flags_images folder.
    - Save the data in a JSON file (flags_data.json).