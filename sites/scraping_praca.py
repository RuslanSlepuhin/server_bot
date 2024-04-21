import asyncio
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from sites.scraping_hh import HHGetInformation


class PracaGetInformation(HHGetInformation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://praca.by"
        self.source_title_name = "https://praca.by"
        self.source_short_name = "PRACA"
        self.search_words = ["Разработчик", "Дизайнер", "Аналитик", "Рекрутер"]
        self.word = None
        self.additional = (
            f"search/vacancies/?"
            f"page=**page&"
            f"search[query]=**word&"
            f"search[query-text-params][headline]=0&"
            f"form-submit-btn=Искать"
        )
        self.link_x_path = "//a[@class='vac-small__title-link']"

    async def get_info(self, how_much_pages=6, separator="+"):
        await self.get_browser()
        for word in self.search_words:
            self.word = word
            # not remote
            for self.page_number in range(0, how_much_pages - 1):
                url = f'{self.base_url}{self.additional.replace("**word", self.word).replace("**page", str(self.page_number))}'
                if self.debug and self.main_class:
                    await self.main_class.bot.send_message(
                        self.chat_id, f"Url: {url}", disable_web_page_preview=True
                    )
                self.browser.get(url)
                await asyncio.sleep(2)
                vacancy_exists_on_page = await self.get_link_message(
                    self.browser.page_source
                )
                if not vacancy_exists_on_page:
                    break
        if self.bot_dict:
            await self.bot.send_message(
                self.chat_id,
                f"{self.source_title_name} parsing: Done!",
                disable_web_page_preview=True,
            )
        pass

    async def get_link_message(self, raw_content):
        def get_links() -> list:
            """
            Retrieves the list of all the links in found vacancies webpage.
            Waits until all the items in the list have been found.
            """
            all_links = []

            try:
                links_ = WebDriverWait(self.browser, 10).until(
                    ec.presence_of_all_elements_located((By.XPATH, self.link_x_path))
                )
                for element in links_:
                    link_ = element.get_attribute("href")
                    all_links.append(link_)
            except Exception as ex:
                print("get_links -> ", ex)
            if all_links:
                print("get_links -> XPATH: ", self.link_x_path)

            return all_links

        links = []
        for _ in range(2):
            try:
                links = get_links()
            except TimeoutException:
                continue
            else:
                break
        for link in links:
            self.list_links.append(link)
        if self.list_links:
            if self.bot_dict:
                self.current_message = await self.bot.send_message(
                    self.chat_id,
                    f"{self.source_short_name}:\nПо слову {self.word} найдено {len(self.list_links)} вакансий на странице {self.page_number + 1}",
                    disable_web_page_preview=True,
                )

            # --------------------- LOOP -------------------------
            self.written_vacancies = 0
            self.rejected_vacancies = 0

            await self.get_content_from_link()
            # ----------------------- the statistics output ---------------------------
            self.written_vacancies = 0
            self.rejected_vacancies = 0
            return True
        else:
            return False

    async def get_vacancy_data(self, vacancy_url, return_raw_dictionary):

        self.browser.get(vacancy_url)
        soup = BeautifulSoup(self.browser.page_source, "lxml")

        title = soup.find("h1", class_="no-margin-top no-margin-bottom").get_text()
        vacancy = title

        salary_ = soup.find("div", class_="vacancy__salary")
        salary = salary_.get_text().lstrip() if salary_ else None

        time_of_public_ = soup.find_all("div", class_="common-info__item")[1].find(
            "time"
        )["datetime"][:-5]
        datetime_obj = datetime.strptime(time_of_public_, "%Y-%m-%dT%H:%M:%S")
        date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

        company = soup.find("div", class_="vacancy__org-name").get_text().lstrip()
        company_link = soup.find("div", class_="vacancy__org-name").find("a")["href"]

        city = soup.find("div", class_="vacancy__city").get_text()

        contacts = None
        contact_ = soup.find("div", id="showContacts")
        if "Электронная почта:" in contact_.get_text():
            contacts = contact_.find("a").get_text()

        experience = soup.find("div", class_="vacancy__desc").get_text(strip=True)
        body = soup.find("div", class_="description wysiwyg-st").get_text(strip=True)

        english = None
        english_ = soup.find("div", class_="vacancy__languages")
        if english_:
            english = english_.find("div", class_="vacancy__desc").get_text()

        job_type_ = (
            soup.find("b", string="Характер работы:")
            .next_sibling.get_text(strip=True)
            .split(",")
        )
        job_type = await self.collect_job_type(job_type_)

        relocation = None
        try:
            await self.collect_result_dict(
                title,
                body,
                vacancy,
                vacancy_url,
                company,
                company_link,
                english,
                relocation,
                job_type,
                city,
                salary,
                experience,
                date,
                contacts,
                return_raw_dictionary,
                vacancy=vacancy,
            )
        except Exception as ex:
            print("get_vacancy_data (2) -> ", ex)
            pass

    @staticmethod
    async def collect_job_type(job_type_: list) -> list:
        job_type = []
        for job in job_type_:
            if "на территории работодателя" in job.lower():
                job_type.append("office")
            elif "работа на дому / удаленная работа" in job.lower():
                job_type.append("remote")
            elif "разъездной" in job.lower():
                job_type.append("flexible")
        return job_type
