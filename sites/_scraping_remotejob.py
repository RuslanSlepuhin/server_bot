import asyncio
from datetime import datetime

from bs4 import BeautifulSoup
from sites.scraping_hh import HHGetInformation


class RemoteJobGetInformation(HHGetInformation):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_url = "https://remote-job.ru/"
        self.source_title_name = "https://remote-job.ru/"
        self.source_short_name = "REMOTE-JOB"
        self.search_words = [
            "Дизайн",
            "Разработчик",
            "Developer",
            "Аналитик",
            "Рекрутер",
            "Mobile",
            "Marketing",
            "Product & Project manager",
            "DevOps",
            "Support",
            "QA",
            "GameDev",
        ]
        self.word = None
        self.additional = (
            f"search?search[query]=**word&"
            f"search[searchType]=vacancy&"
            f"page=**page"
        )

        self.link_x_path = "//div[@class='vacancy_item']//a[@target='_blank']"

    async def get_info(self, how_much_pages=6, separator="+"):
        await self.get_browser()
        for word in self.search_words:
            self.word = word
            # not remote
            for self.page_number in range(1, how_much_pages):
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

    async def get_vacancy_data(self, vacancy_url, return_raw_dictionary):

        self.browser.get(vacancy_url)
        soup = BeautifulSoup(self.browser.page_source, "lxml")

        title_ = (
            soup.find("div", class_="col-md-12 col-sm-12 col-lg-12 col-xs-12")
            .find("h1")
            .get_text()
            .split("\n")
        )
        title_ = list(filter(None, map(str.strip, title_)))
        title = title_[0].strip()
        job_type = title_[1].strip() if len(title_) > 1 else None

        body_ = soup.find("div", class_="panel-body").find_all("br")
        body = [br_tag.next_sibling for br_tag in body_]
        body = " ".join(list(filter(None, map(str.strip, body))))

        vacancy = title

        company = (
            soup.find("div", class_="col-md-12 col-sm-12 col-lg-12 col-xs-12")
            .find("a")
            .get_text(strip=True)
        )
        company_link = (
            soup.find("div", class_="col-md-12 col-sm-12 col-lg-12 col-xs-12")
            .find("a")["href"]
            .lstrip()
        )

        salary_experience = soup.find("div", class_="row m-y-1").find_all(
            "div", class_="col-md-4"
        )
        salary = salary_experience[0].find("b").get_text(strip=True)
        experience = salary_experience[1].find("b").get_text(strip=True)
        salary = " ".join(salary.split())

        time_of_public = (
            soup.find("div", class_="col-xs-5 col-sm-5 col-md-5 col-lg-5 text-left")
            .find("p")
            .get_text(strip=True)
        )
        date = self.normalize_date(time_of_public)

        english = None
        relocation = None
        city = None
        contacts = None

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

    def normalize_date(self, date):
        convert = {
            "января": "01",
            "февраля": "02",
            "марта": "03",
            "апреля": "04",
            "мая": "05",
            "июня": "06",
            "июля": "07",
            "августа": "08",
            "сентября": "09",
            "октября": "10",
            "ноября": "11",
            "декабря": "12",
        }

        date = date.split()
        month = date[1]
        day = date[0]
        year = date[2]

        date = datetime(int(year), int(convert[month]), int(day), 12, 00, 00)

        return date
