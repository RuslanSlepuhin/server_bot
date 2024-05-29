import re
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from sites.scraping_hh import HHGetInformation

class FinderGetInformation(HHGetInformation):

    async def get_content(self, *args, **kwargs):
        self.base_url = "https://finder.work/vacancies?"
        self.additional = ("categories=7&"
                           "categories=1&"
                           "categories=10&"
                           "categories=2&"
                           "categories=8")
        self.pages_listing = "&page=**page"
        self.source_title_name = "https://finder.work"
        self.searching_text_separator = "%20"
        self.source_short_name = "FINDER"

        await super().get_content(*args, **kwargs)

    async def get_info(self, how_much_pages=19, separator="+"):
        await super().get_browser()

        for self.page_number in range(0, how_much_pages):
            url = f'{self.base_url}{self.additional}'
            page_url = f'{url}{self.pages_listing.replace("**page", str(self.page_number))}'
            if self.debug:
                await self.main_class.bot.send_message(self.chat_id, f"Url: {url}",
                                                       disable_web_page_preview=True)
            self.now = datetime.now().time().strftime('%H:%M:%S') + str(self.page_number)
            if self.page_number == 0:
                self.browser.get(url)
                time.sleep(2)
            elif self.page_number > 0:
                self.browser.get(page_url)
                time.sleep(2)

            vacancy_exists_on_page = await self.get_link_message(self.browser.page_source)
            if not vacancy_exists_on_page:
                break

        if self.bot_dict:
            await self.bot.send_message(self.chat_id, f'{self.source_title_name} parsing: Done!',
                                        disable_web_page_preview=True)

    async def get_link_message(self, raw_content):
        self.links_x_path = ["//a[contains(@href, '/vacancies/') and @target='_blank']"]
        return await super().get_link_message(raw_content)

    async def get_vacancy_data(self, vacancy_url, return_raw_dictionary):
        vacancy_x_path = "//div[@class='vacancy-info-header']/h1"
        body_x_path = "//div[@class='vacancy-info-body vacancy-info__body']"
        company_x_path = "//div[@class='company__title']/a"
        time_job_x_path = "//div[@class='vacancy-info-header__publication-date']"
        salary_x_path = "//div[@class='vacancy-info-header']/h2"
        experience_x_path = "//div[contains(@class, 'flex flex-row flex-wrap')]/a"

        try:
            self.browser.get(vacancy_url)
            time.sleep(3)
            vacancy = self.browser.find_element(By.XPATH, vacancy_x_path).text
        except:
            vacancy = ''
        if vacancy:
            title = vacancy
            body = ""
            try:
                body_list = self.browser.find_elements(By.XPATH, body_x_path)
                for i in body_list:
                    body += f"{i.text}\n"
                body=body.replace("0\n", "")
            except:
                body = ''

            try:
                company = self.browser.find_element(By.XPATH, company_x_path).text
            except:
                company = ''

            try:
                time_job = self.browser.find_element(By.XPATH, time_job_x_path).text
            except:
                time_job = ''

            try:
                salary = self.browser.find_element(By.XPATH, salary_x_path).text
            except:
                salary = ''

            try:
                experience = self.browser.find_element(By.XPATH, experience_x_path).text
            except:
                experience = ''

            time_of_public = self.convert_date(time_job)

            await self.collect_result_dict(
                title, body, vacancy, vacancy_url, company, "", "", "", "",
                "", salary, experience, time_of_public, "", return_raw_dictionary, vacancy=vacancy)
        else:
            self.response = {}

    def convert_date(self, date):
        date = date.split(' ')
        if date[1] == 'сегодня':
            date = datetime.now()
        elif date[1] == 'вчера':
            date = datetime.now()-timedelta(days=1)
        elif date[1] == 'неделю':
            date = datetime.now()-timedelta(days=7)
        elif re.findall(r'д[е]{0,1}н[ьейя]{1,2}', date[2]):
            date = datetime.now()-timedelta(days=int(date[1]))
        elif re.findall(r'месяц[ева]{0,2}', date[2]):
            date = datetime.now() - timedelta(days=int(date[1]*30))
        return date


