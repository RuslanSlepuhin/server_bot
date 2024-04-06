import asyncio
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from utils.additional_variables.additional_variables import (admin_database,
                                                             archive_database)

from sites.scraping_hh import HHGetInformation


class WellFoundGetInformation(HHGetInformation):
    """Парсинг https://wellfound.com"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://wellfound.com/location/united-states?page="
        self.source_title_name = "https://wellfound.com"
        self.source_short_name = "WELLFOUND"
        self.job_url = "https://wellfound.com/jobs"

    async def get_info(self, how_much_pages=65, separator=None):
        await self.get_browser()

        while self.page != how_much_pages:
            url = self.base_url + str(self.page_number)
            if self.debug:
                await self.main_class.bot.send_message(
                    self.chat_id, f"Url: {url}", disable_web_page_preview=True
                )
            self.browser.get(url)
            await asyncio.sleep(2)
            soup = BeautifulSoup(self.browser.page_source, "lxml")

            current_page = soup.find("title").get_text()
            if current_page == "404: We couldn't find what you were looking for":
                break
            elif current_page == "wellfound.com":
                continue
            companies_per_page = soup.find_all("div", class_="styles_result__rPRNG")
            vacancy_url_list = []
            for company in companies_per_page:
                info_div = company.find_all("div", class_="styles_jobListing__PLqQ_")
                for vac in info_div:
                    job_link = vac.find("a", class_="styles_component__UCLp3").get(
                        "href"
                    )
                    vac_url = self.job_url + job_link
                    vacancy_url_list.append(vac_url)
                    await self.get_vacancy_data(
                        vacancy_url=vac_url, return_raw_dictionary=None
                    )
            vacancy_exists_on_page = await self.get_link_message(vacancy_url_list)
            if not vacancy_exists_on_page:
                break
            self.page += 1

        if self.bot_dict:
            await self.bot.send_message(
                self.chat_id,
                f"{self.source_title_name} parsing: Done!",
                disable_web_page_preview=True,
            )

    async def get_vacancy_data(self, vacancy_url, return_raw_dictionary):
        self.browser.get(vacancy_url)
        soup_vac = BeautifulSoup(self.browser.page_source, "lxml")
        current_page = soup_vac.find("title").get_text()
        if current_page != "410: What you were looking for is no longer available":
            title = vacancy_url.find(
                "h1", class_="inline text-xl font-semibold text-black"
            ).get_text()
            vacancy = title
            salary = vacancy_url.find(
                "div", class_="mt-2 text-lg font-medium text-gray-800"
            ).get_text()

            public_time = vacancy_url.find(
                "div", class_="mb-4 mt-1 text-sm font-medium text-gray-600"
            ).get_text()
            date = self.normalize_date(public_time.split(": ")[1])

            company = vacancy_url.find(
                "h2", class_="mt-1 text-lg font-bold text-black underline"
            ).get_text()
            company_link = self.source_title_name + vacancy_url.find(
                "a", rel="noopener noreferrer", target="_blank"
            ).get("href")

            location = (
                vacancy_url.find("h3", class_="text-md font-semibold")
                .find_next()
                .get_text()
                .split("•")
            )
            city = location[1] if len(location) > 1 else location[0]

            job_type = (
                vacancy_url.find("h3", string="Job Type")
                .find_parent()
                .get_text(separator="\n")
                .split("\n")[1]
            )
            relocation = (
                vacancy_url.find("h3", string="Relocation").find_next("span").get_text()
            )
            body = vacancy_url.find("div", id="job-description").get_text()
            vacancy_url = vacancy_url.find("link", rel="canonical").get("href")

            get_experience = vacancy_url.find(
                "span", class_="text-xl font-medium text-gray-500"
            )
            experience = get_experience.get_text() if get_experience else None

            english = None
            contacts = None

            # -------------------- compose one writting for ione vacancy ----------------
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
                vacancy=vacancy,
            )

    async def get_content_from_link(self, return_raw_dictionary=False):
        self.found_by_link = 0
        for link in self.list_links:
            try:
                vacancy_url = link.get("href")
            except:
                vacancy_url = link
            print("url", vacancy_url)
            # pre-checking by link
            check_vacancy_not_exists = self.db.check_exists_message_by_link_or_url(
                vacancy_url=vacancy_url, table_list=[admin_database, archive_database]
            )
            if (
                check_vacancy_not_exists
                or not check_vacancy_not_exists
                and return_raw_dictionary
            ) and vacancy_url not in self.links_in_past:
                self.links_in_past.append(vacancy_url)
                await self.get_vacancy_data(vacancy_url, return_raw_dictionary)
            else:
                self.found_by_link += 1
                print("vacancy link exists")

    async def get_link_message(self, raw_content):
        for vacancy_link in raw_content:
            self.list_links.append(vacancy_link)
        if self.list_links:
            if self.bot_dict:
                self.current_message = await self.bot.send_message(
                    self.chat_id,
                    f"{self.source_short_name}:\nнайдено {len(self.list_links)} вакансий на странице {self.page_number}",
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

    async def normalize_date(self, published_text: str) -> datetime:
        today = datetime.now().replace(hour=12, minute=0, second=0)
        if published_text == "today":
            return today
        elif published_text == "yesterday":
            return today - timedelta(days=1)
        int_date = int(published_text.split()[0])
        if "day" in published_text:
            return today - timedelta(days=int_date)
        elif "week" in published_text:
            return today - timedelta(weeks=int_date)
        elif "month" in published_text:
            return today - timedelta(days=30 * int_date)
