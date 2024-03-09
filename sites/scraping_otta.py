import asyncio

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from db_operations.scraping_db import DataBaseOperations
from helper_functions import helper_functions as helper
from helper_functions.helper_functions import edit_message, send_message
from helper_functions.parser_find_add_parameters.parser_find_add_parameters import (
    FinderAddParameters,
)
from settings.browser_settings import options
from sites.write_each_vacancy_to_db import HelperSite_Parser
from utils.additional_variables.additional_variables import (
    admin_database,
    archive_database,
    sites_search_words,
)


class OttaGetInformation:
    USERMAIL = "vasia_stallion@mail.ru"
    PASSWORD = "Vasia01010"

    def __init__(self, **kwargs):

        self.report = kwargs["report"] if "report" in kwargs else None
        self.bot_dict = kwargs["bot_dict"] if "bot_dict" in kwargs else None
        self.helper_parser_site = HelperSite_Parser(report=self.report)
        self.search_words = (
            [kwargs["search_word"]] if "search_word" in kwargs else sites_search_words
        )
        self.db = DataBaseOperations(report=self.report)
        self.db_tables = None
        self.options = None
        self.page = None
        self.page_number = 1
        self.current_message = None
        self.msg = None
        self.written_vacancies = 0
        self.rejected_vacancies = 0
        if self.bot_dict:
            self.bot = self.bot_dict["bot"]
            self.chat_id = self.bot_dict["chat_id"]
        self.browser = None
        self.find_parameters = FinderAddParameters()
        self.count_message_in_one_channel = 1
        self.found_by_link = 0
        self.response = {}
        self.helper = helper

    async def get_content(self, db_tables=None):
        self.db_tables = db_tables
        try:
            await self.get_info()
        except Exception as ex:
            print(f"Error: {ex}")
            if self.bot:
                await self.bot.send_message(self.chat_id, f"Error: {ex}")

        if self.report and self.helper:
            try:
                await self.report.add_to_excel()
                await self.helper.send_file_to_user(
                    bot=self.bot,
                    chat_id=self.chat_id,
                    path=self.report.keys.report_file_path["parsing"],
                )
            except Exception as ex:
                print(f"Error: {ex}")
                if self.bot:
                    await self.bot.send_message(self.chat_id, f"Error: {ex}")
        self.browser.quit()

    async def login(self):
        self.browser.get("https://app.otta.com/jobs/")

        sign = self.browser.find_elements(
            By.CSS_SELECTOR, "h1[data-testid='login-heading']"
        )

        while len(sign) > 0:
            email_input = self.browser.find_element(By.ID, "email")
            pass_input = self.browser.find_element(By.ID, "password")
            confirm_input = self.browser.find_element(
                By.CSS_SELECTOR, "button[data-testid='login-button']"
            )

            email_input.send_keys(self.USERMAIL)
            pass_input.send_keys(self.PASSWORD)
            confirm_input.click()
            await asyncio.sleep(1.5)
            sign = self.browser.find_elements(
                By.CSS_SELECTOR, "h1[data-testid='login-heading']"
            )

    async def get_info(self):
        options.add_argument("--headless=new")
        try:
            self.browser = webdriver.Chrome(options=options)
        except WebDriverException:
            self.browser = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        # -------------------- check what is current session --------------
        self.current_session = await self.helper_parser_site.get_name_session()

        await self.login()

        self.browser.get("https://app.otta.com/jobs/")
        self.browser.implicitly_wait(3)

        next_btn_sel = "button[data-testid='next-button']"
        next_btn = self.browser.find_elements(By.CSS_SELECTOR, next_btn_sel)

        vac_count = 0

        while len(next_btn) > 0:
            vac_count += 1

            await asyncio.sleep(1)

            await self.get_content_from_link(self.browser.page_source)

            if self.bot_dict:
                await self.bot.send_message(
                    self.chat_id,
                    f"Parsing {self.browser.current_url}",
                    disable_web_page_preview=True,
                )

            next_btn[0].click()
            next_btn = self.browser.find_elements(By.CSS_SELECTOR, next_btn_sel)

        if self.bot_dict:
            await self.bot.send_message(
                self.chat_id,
                f"otta.com parsing: Done! Parsed {vac_count} vacancies",
                disable_web_page_preview=True,
            )

    async def get_content_from_link(self, raw_content, return_raw_dictionary=False):
        vacancy_url = self.browser.current_url
        print(f"{vacancy_url}", sep="\n")

        check_vacancy_not_exists = self.db.check_exists_message_by_link_or_url(
            vacancy_url=vacancy_url, table_list=[admin_database, archive_database]
        )
        if (
            check_vacancy_not_exists
            or not check_vacancy_not_exists
            and return_raw_dictionary
        ):
            try:
                soup = BeautifulSoup(raw_content, "html.parser")
            except Exception as ex:
                print(f"error in browser.get {ex}")
            else:
                vacancy = title = ""
                try:
                    title = soup.find(
                        "h2", attrs={"data-testid": "job-title"}
                    ).get_text()
                    vacancy = title.split(",")[0]

                    level = soup.find(
                        "div", attrs={"data-testid": "experience-section"}
                    ).get_text()
                    vacancy = f"{vacancy}: {level}"
                except Exception as e:
                    print(f"error vacancy: {e}")

                company = ""
                company_url = ""
                try:
                    company_tag = soup.find(
                        "h2", attrs={"data-testid": "job-title"}
                    ).find("a")
                    company_url = company_tag.get("href").split("?")[0]
                    company = company_tag.get_text()
                except Exception as e:
                    print(f"error company: {e}")

                body = ""
                try:
                    job_involves = soup.findAll(
                        "li", attrs={"data-testid": "job-involves-bullet"}
                    )
                    body = "\n".join(job.text for job in job_involves)
                except Exception as e:
                    print(f"error body: {e}")

                tags = ""
                try:
                    tags_list = soup.find(
                        "div", attrs={"data-testid": "job-technology-used"}
                    ).find_all("div")
                    if len(tags_list) > 0:
                        tags = ", ".join(tag.text for tag in tags_list)
                except Exception as e:
                    print(f"error tags: {e}")

                salary = ""
                try:
                    salary_section = soup.find(
                        "div", attrs={"data-testid": "salary-section"}
                    ).find("p")
                    if salary_section:
                        sums = salary_section.findAll("span")
                        if sums:
                            salary = " - ".join(s.text for s in sums)
                        else:
                            salary = salary_section.get_text()
                except Exception as e:
                    print(f"error salary: {e}")

                experience = ""
                try:
                    requirements = soup.findAll(
                        "li", attrs={"data-testid": "job-requirement-bullet"}
                    )
                    experience = "\n".join(req.text for req in requirements)
                except Exception as e:
                    print(f"error experience: {e}")

                city = ""
                try:
                    cities = soup.findAll(
                        "div", attrs={"data-testid": "job-location-tag"}
                    )
                    city = " ".join(c.text for c in cities)
                except Exception as e:
                    print(f"error job_type: {e}")

                results_dict = {
                    "chat_name": "https://app.otta.com/",
                    "title": title,
                    "body": body,
                    "vacancy": vacancy,
                    "vacancy_url": vacancy_url,
                    "company": company,
                    "company_link": company_url,
                    "english": "B2",
                    "relocation": "",
                    "job_type": "",
                    "city": city,
                    "salary": salary,
                    "experience": experience,
                    "time_of_public": "",
                    "contacts": "",
                    "tags": tags,
                    "session": self.current_session,
                }

                if not return_raw_dictionary:
                    response = await self.helper_parser_site.write_each_vacancy(
                        results_dict
                    )

                    await self.output_logs(
                        about_vacancy=response, vacancy=vacancy, vacancy_url=vacancy_url
                    )
                    # return response
                    self.response = response
                else:
                    self.response = results_dict

        else:
            self.found_by_link += 1
            print("vacancy link exists")

    async def output_logs(self, about_vacancy, vacancy, vacancy_url=None):
        additional_message = ""

        if about_vacancy["response"]["vacancy"] in [
            "found in db by link",
            "found in db by title-body",
        ]:
            additional_message = f"-exists in db\n\n"
            self.rejected_vacancies += 1

        elif about_vacancy["response"]["vacancy"] == "no vacancy by anti-tags":
            additional_message = f"-ANTI-TAG by vacancy\n\n"
            self.rejected_vacancies += 1

        elif about_vacancy["response"]["vacancy"] == "written to db":
            if about_vacancy["profession"]:
                profession = about_vacancy["profession"]
                prof_str = ", ".join(profession["profession"])
                additional_message = f"<b>+w: {prof_str}</b>\n{vacancy_url}\n{profession['tag']}\n{profession['anti_tag']}\n\n"
                self.written_vacancies += 1
            else:
                additional_message = "written to db"
                self.written_vacancies += 1

        if self.bot_dict:
            if (
                len(
                    f"{self.current_message}\n{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"
                )
                < 4096
            ):
                new_text = f"\n{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"

                self.current_message = await edit_message(
                    bot=self.bot, text=new_text, msg=self.current_message
                )
            else:
                new_text = f"{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"
                self.current_message = await send_message(
                    bot=self.bot, chat_id=self.chat_id, text=new_text
                )
