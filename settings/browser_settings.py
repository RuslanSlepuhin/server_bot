from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

options = Options()
# options.headless = True
# options.no_sandbox = True
options.add_argument('--headless')
options.add_argument('--no-sandbox')
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--window-size=1920x1080")
# options.add_argument('window-size=1920x935')
# chromeOptions.add_argument('window-size=1920x935')
# chromeOptions.add_argument("--remote-debugging-port=9222")
# browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# browser = webdriver.Firefox(
#     executable_path='/root/itcoty_bot/server_bot/settings/firefox_driver/geckodriver',
#     options=options
# )
browser = webdriver.Chrome(
    executable_path='/root/itcoty_bot/server_bot/utils/chromedriver/chromedriver',
    options=options
)
