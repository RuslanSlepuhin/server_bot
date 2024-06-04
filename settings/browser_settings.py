from selenium import webdriver
from _debug import debug

options = webdriver.ChromeOptions()
if not debug:
    options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--verbose')

chrome_driver_path = '/root/itcoty_bot/server_bot/utils/chromedriver/chromedriver'
