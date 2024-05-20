from sites.scraping_hh import HHGetInformation
import asyncio
from datetime import datetime


class HHITGetInformation(HHGetInformation):

    async def get_content(self, *args, **kwargs):
        self.additional = (
                f"/search/vacancy?"
                f"L_save_area=true&" 
                f"text=&"
                f"industry=7&"
                f"area=0&"
                f"experience=doesNotMatter&"
                f"order_by=publication_time&"
                f"professional_role=96&"
                f"search_period=3&"
                f"items_on_page=100&"
                f"hhtmFrom=vacancy_search_filter"
        )
        self.pages_listing = self.additional.replace(
            "hhtmFrom=vacancy_search_filter",
            "page=**page"
        )
        await super().get_content(*args, **kwargs)


    async def get_info(self, how_much_pages=20, separator="+"):
        separator = separator if not self.searching_text_separator else self.searching_text_separator
        await self.get_browser()

        self.words_pattern = [self.words_pattern] if type(self.words_pattern) is str else self.words_pattern
        self.word = "ИТ. Программист, разработчик"
        for self.page_number in range(0, how_much_pages):
            url = f'{self.base_url}{self.additional}'
            page_url = f'{self.base_url}{self.pages_listing.replace("**page", str(self.page_number))}'
            if self.debug:
                await self.main_class.bot.send_message(self.chat_id, f"Url: {url}",
                                                       disable_web_page_preview=True)
            self.now = datetime.now().time().strftime('%H:%M:%S') + " -->" + str(self.page_number)
            if self.page_number == 0:
                self.browser.get(url)
                await asyncio.sleep(2)
            elif self.page_number > 0:
                self.browser.get(page_url)
                await asyncio.sleep(2)

            vacancy_exists_on_page = await self.get_link_message(self.browser.page_source)
            if not vacancy_exists_on_page:
                break

        if self.bot_dict:
            await self.bot.send_message(self.chat_id, f'{self.source_title_name} parsing: Done!',
                                        disable_web_page_preview=True)
