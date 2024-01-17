from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from settings.browser_settings import options, chrome_driver_path
from utils.additional_variables.additional_variables import sites_search_words, how_much_pages
from sites.scraping_hh import HHGetInformation

class HHKzGetInformation(HHGetInformation):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def get_info(self):
        await self.get_browser()
        # -------------------- check what is current session --------------
        self.current_session = await self.helper_parser_site.get_name_session()
        for word in self.search_words:
            self.word = word
            self.page_number = 0
            link = f'https://hh.kz/search/vacancy?text={self.word}&from=suggest_post&salary=&schedule=remote&no_magic=true&ored_clusters=true&enable_snippets=true&search_period=1&excluded_text='
            if self.bot_dict:
                await self.bot.send_message(self.chat_id, link, disable_web_page_preview=True)

            try:
                self.browser.get(link)
            except Exception as e:
                print('bot could not to get the link', e)

            try:
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except:
                pass
            await self.get_link_message(self.browser.page_source)

            till = how_much_pages
            for self.page_number in range(1, till):
                try:
                    if self.bot_dict:
                        await self.bot.send_message(self.chat_id, f'https://hh.kz/search/vacancy?text={self.word}&from=suggest_post&salary=&schedule=remote&no_magic=true&ored_clusters=true&enable_snippets=true&search_period=1&excluded_text=&page={self.page_number}&hhtmFrom=vacancy_search_list',
                                              disable_web_page_preview=True)
                    self.browser.get(f'https://hh.kz/search/vacancy?text={self.word}&from=suggest_post&salary=&schedule=remote&no_magic=true&ored_clusters=true&enable_snippets=true&search_period=1&excluded_text=&page={self.page_number}&hhtmFrom=vacancy_search_list')
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    vacancy_exists_on_page = await self.get_link_message(self.browser.page_source)
                    if not vacancy_exists_on_page:
                        break
                except:
                    break
        if self.bot_dict:
            await self.bot.send_message(self.chat_id, 'hh.kz parsing: Done!', disable_web_page_preview=True)

    async def get_content_by_link_alone(self, link):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            self.browser.get(link)
        except Exception as e:
            print(e)
            if self.bot_dict:
                await self.bot.send_message(self.chat_id, str(e))
            return False
        try:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            pass
        self.browser.quit()
