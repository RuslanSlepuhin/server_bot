import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class ChatGPTParserPind:

    def __init__(self):
        self.pind_url = "https://www.phind.com/"

    def get_browser(self):
        options = None
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.get_pind()

    def get_pind(self):
        self.browser.get(url=self.pind_url)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.send_first_request()

    def send_dialog_request(self):
        pass

    def send_first_request(self):
        start_field = self.browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[1]/div[2]/div/form/div[1]/textarea')
        start_field.send_keys('Hello')
        search_button = self.browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/div[1]/div[2]/div/form/div[1]/div[2]/button[2]')
        search_button.click()
        return self.get_answer()

    def get_answer(self):
        answer_field = self.browser.find_element(By.XPATH, '')

if __name__ == "__main__":
    chat = ChatGPTParserPind()
    chat.get_browser()




