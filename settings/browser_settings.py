from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service as ChromeService


options = Options()
options.headless = True
options.no_sandbox = True
# chromeOptions.add_argument('window-size=1920x935')

# chromeOptions.add_argument("--remote-debugging-port=9222")
# chromeOptions.add_argument('--disable-dev-shm-usage')

# browser = webdriver.Chrome(
#     executable_path='/root/itcoty_bot/server_bot/utils/chromedriver/chromedriver',
#     chrome_options=chromeOptions
# )
options = Options()
options.headless = True
# options.add_argument('window-size=1920x935')
# browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser = webdriver.Firefox(
    executable_path='/root/itcoty_bot/server_bot/settings/firefox_driver/geckodriver',
    options=options
)

# options = Options()
# options.add_argument('headless')
# options.add_argument('--no-sandbox')
# options.add_argument('window-size=1920x935')
# browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)