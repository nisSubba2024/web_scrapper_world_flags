"""
 * //////////////////////////////////////////////////////////////////////
 *      PROGRAM: WORLD_FLAGS/MAIN.PY
 *      Written by Nishan Subba
 *      GitHub: @nisSubba2024
 *      Purpose: Web scrapper for world flags
 *      Last Date Modified: Dec 31, 2024
 * //////////////////////////////////////////////////////////////////////
"""
from flag_scrapper import WorldFlagScrapper

if __name__ == '__main__':
    page_url = "https://www.worldometers.info/geography/flags-of-the-world"
    world_scrapper = WorldFlagScrapper(page_url)
    world_scrapper.url_connection()
    world_scrapper.flags_wrapper()
    world_scrapper.scrap_flags()
    world_scrapper.create_image_folder()
    world_scrapper.download_flags()
    world_scrapper.create_json_database()
