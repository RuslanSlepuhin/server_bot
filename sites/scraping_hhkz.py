from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from settings.browser_settings import options, chrome_driver_path
from utils.additional_variables.additional_variables import sites_search_words, how_much_pages
from sites.scraping_hh import HHGetInformation

class HHKzGetInformation(HHGetInformation):

    async def get_content(self, *args, **kwargs):
        self.base_url = "https://hh.kz"
        await super().get_content(*args, **kwargs)

