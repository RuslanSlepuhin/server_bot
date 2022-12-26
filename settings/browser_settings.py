from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService


chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument('--no-sandbox')
# chromeOptions.add_argument("--remote-debugging-port=9222")
chromeOptions.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(
    executable_path='/root/itcoty_bot/server_bot/utils/chromedriver/chromedriver',
    chrome_options=chromeOptions
)