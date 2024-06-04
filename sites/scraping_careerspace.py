import re
import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from sites.write_each_vacancy_to_db import HelperSite_Parser
from settings.browser_settings import options, chrome_driver_path
from utils.additional_variables.additional_variables import admin_database, archive_database


class CareerSpaceGetInformation:

    def __init__(self, **kwargs):
        self.report = kwargs['report'] if 'report' in kwargs else None
        self.search_words = kwargs['search_word'] if 'search_word' in kwargs else None
        self.bot_dict = kwargs['bot_dict'] if 'bot_dict' in kwargs else None
        self.db = kwargs['db'] if 'db' in kwargs else None
        self.helper = kwargs['helper'] if 'helper' in kwargs else None
        self.helper_parser_site = HelperSite_Parser(report=self.report, db=self.db)
        self.db_tables = None
        self.options = None
        self.current_message = None
        self.written_vacancies = 0
        self.rejected_vacancies = 0
        if self.bot_dict:
            self.bot = self.bot_dict['bot']
            self.chat_id = self.bot_dict['chat_id']
        self.browser = None
        self.main_url = 'https://careerspace.app'
        self.count_message_in_one_channel = 1
        self.found_by_link = 0
        self.response = None
        self.current_session = None

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
                    bot=self.bot, chat_id=self.chat_id,
                    path=self.report.keys.report_file_path['parsing'],
                )
            except Exception as ex:
                print(f"Error: {ex}")
                if self.bot:
                    await self.bot.send_message(self.chat_id, f"Error: {ex}")
        self.browser.quit()

    async def get_info(self):
        try:
            self.browser = webdriver.Chrome(
                executable_path=chrome_driver_path,
                options=options
            )
        except:
            self.browser = webdriver.Chrome(
                service=Service(
                    ChromeDriverManager().install()),
                options=options
            )
        self.current_session = await self.helper_parser_site.get_name_session() if self.db else None
        if self.bot_dict:
            await self.bot.send_message(
                self.chat_id,
                'https://careerspace.app',
                disable_web_page_preview=True
            )
        self.browser.get('https://careerspace.app/jobs?'
                         'functions%5B%5D=8&'
                         'functions%5B%5D=14&'
                         'functions%5B%5D=7&'
                         'functions%5B%5D=19&'
                         'functions%5B%5D=13&'
                         'area=everywhere&'
                         'isPreFilter=true')
        for _ in range(50):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        try:
            vacancy_exists_on_page = await self.get_link_message(self.browser.page_source)
        except:
            pass
        if self.bot_dict:
            await self.bot.send_message(
                self.chat_id,
                'careerspace.app parsing: Done!',
                disable_web_page_preview=True
            )

    async def get_link_message(self, raw_content):
        soup = BeautifulSoup(raw_content, 'lxml')
        open_links = soup.find_all('div', class_='job-card job-card job-card--main')
        self.list_links = list(set(open_links))

        if self.list_links:
            if self.bot_dict:
                self.current_message = await self.bot.send_message(
                    self.chat_id,
                    f'careerspace.app:\nНайдено {len(self.list_links)} вакансий',
                    disable_web_page_preview=True
                )
            # --------------------- LOOP -------------------------
            self.written_vacancies = 0
            self.rejected_vacancies = 0
            try:
                await self.get_content_from_link()
            except Exception as e:
                print(f"Error: {e}")
                if self.bot:
                    await self.bot.send_message(self.chat_id, f"Error: {e}")
            # ----------------------- the statistics output ---------------------------
            return True
        else:
            return False

    async def get_content_from_link(self):
        check_vacancy_not_exists = True
        links = []
        soup = None
        self.found_by_link = 0
        for link in self.list_links:
            found_vacancy = True
            try:
                vacancy_url = link.find('a').get('href')
                vacancy_url = self.main_url + vacancy_url
            except:
                vacancy_url = link
                print(f"\n{vacancy_url}\n")

            if self.db:
                check_vacancy_not_exists = self.db.check_exists_message_by_link_or_url(
                    vacancy_url=vacancy_url,
                    table_list=[admin_database, archive_database]
                )
            if check_vacancy_not_exists:
                links.append(vacancy_url)
                try:
                    self.browser.get(vacancy_url)
                    soup = BeautifulSoup(self.browser.page_source, 'lxml')
                except Exception as ex:
                    found_vacancy = False
                    print(f"error in browser.get {ex}")

                if found_vacancy:
                    try:
                        vacancy = soup.find("h1", attrs={"data-testid": "csu-title"}).text
                    except AttributeError as ex:
                        vacancy = ""
                        print(f"Exception occurred: {ex}")

                    # get title --------------------------
                    title = vacancy

                    # get body --------------------------
                    try:
                        body = soup.find("div", class_="j-d__dsc-vl").text.strip()
                    except AttributeError as ex:
                        body = None
                        print(f"Exception occurred: {ex}")

                    # get city and job_format --------------
                    try:
                        job_info = []
                        inner_div = soup.find('div', class_='j-d-h__cities cs-df-alc')
                        city_span = inner_div.find_all('span', class_='job-lb cs-df-alc job-lb--df')
                        for span in city_span:
                            print(span.get_text().strip())
                        for span in city_span:
                            job_info.append(span.get_text(strip=True))
                        city = []
                        job_format = []
                        for i in range(len(job_info)):
                            if job_info[i] == "Удаленно" or job_info[i] == "Гибрид":
                                job_format.append(job_info[i])
                            else:
                                city.append(job_info[i])
                    except AttributeError as ex:
                        job_format = None
                        city = None
                        print(f"AttributeError occurred: {ex}")

                    # get company -------------------------
                    try:
                        company_div = soup.find("div", class_="j-d-h__bl cs-df-alc-jsb")
                        company = company_div.find("span", attrs={"data-v-27ef1e69": ""}).text
                    except AttributeError as ex:
                        company = None
                        print(f"Exception occurred: {ex}")

                    # get salary --------------------------
                    try:
                        salary = soup.find("div", class_="price").text.strip()
                    except AttributeError as ex:
                        salary = None
                        print(f"AttributeError occurred: {ex}")

                    # get relocation ------------------------
                    relocation = ''
                    if re.findall(r'[Rr]elocation', body):
                        relocation = 'релокация'
                    if self.db:
                        self.db.write_to_db_companies([company])

                    # get time of public --------------------
                    time_of_public, published_at = "", ""
                    try:
                        time_of_public = soup.find("meta", attrs={"name": "description"})
                        time_of_public = time_of_public.get("content")
                        time_of_public = time_of_public.split("Дата публикации: ")
                        time_of_public = time_of_public.pop(1).replace(".", "")
                        months = {
                            "января": "january",
                            "февраля": "february",
                            "марта": "march",
                            "апреля": "april",
                            "мая": "may",
                            "июня": "june",
                            "июля": "july",
                            "августа": "august",
                            "сентября": "september",
                            "октября": "october",
                            "ноября": "november",
                            "декабря": "december"
                        }
                        for ru_month, en_month in months.items():
                            if ru_month in time_of_public:
                                published_at = time_of_public.replace(ru_month, en_month)
                                break
                        time_of_public = datetime.strptime(published_at, "%d %B %Y")
                    except AttributeError as ex:
                        time_of_public = ""
                        print(f"AttributeError occurred: {ex}")

                    # -------------------- compose one writting for ione vacancy ----------------
                    results_dict = {
                        'chat_name': 'https://careerspace.app/',
                        'title': title,
                        'body': body,
                        'vacancy': vacancy,
                        'vacancy_url': vacancy_url,
                        'company': company,
                        'company_link': '',
                        'english': '',
                        'relocation': relocation,
                        'job_type': job_format,
                        'city': city,
                        'salary': salary,
                        'experience': '',
                        'time_of_public': time_of_public,
                        'contacts': '',
                        'session': self.current_session
                    }
                    return_raw_dictionary = False
                    if not return_raw_dictionary:
                        response = await self.helper_parser_site.write_each_vacancy(results_dict)
                        print('sort profession (33)')
                        await self.output_logs(
                            about_vacancy=response,
                            vacancy=vacancy,
                            vacancy_url=vacancy_url
                        )
                        self.response = response
                    else:
                        self.response = results_dict
            else:
                self.found_by_link += 1
                print("vacancy link exists")
        if self.found_by_link > 0:
            self.count_message_in_one_channel += self.found_by_link
            if self.bot_dict:
                self.current_message = await self.helper.edit_message(bot=self.bot,
                    text=f"\n---\nfound by link: {self.found_by_link}", msg=self.current_message)

    async def get_content_from_one_link(self, vacancy_url):
        try:
            self.browser = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
        except:
            self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # -------------------- check what is current session --------------
        self.current_session = await self.helper_parser_site.get_name_session()
        self.list_links = [vacancy_url]
        await self.get_content_from_link()
        self.browser.quit()
        return self.response

    async def write_to_db_table_companies(self):
        excel_data_df = pd.read_excel('all_geek.xlsx', sheet_name='Sheet1')
        companies = excel_data_df['hiring'].tolist()
        links = excel_data_df['access_hash'].tolist()
        companies = set(companies)
        if self.db:
            self.db.write_to_db_companies(companies)

    async def output_logs(self, about_vacancy, vacancy, word=None, vacancy_url=None):
        additional_message = ''

        if about_vacancy['response']['vacancy'] in ['found in db by link', 'found in db by title-body']:
            additional_message = f'-exists in db\n\n'
            self.rejected_vacancies += 1
        elif about_vacancy['response']['vacancy'] == 'no vacancy by anti-tags':
            additional_message = f'-ANTI-TAG by vacancy\n\n'
            self.rejected_vacancies += 1
        elif about_vacancy['response']['vacancy'] == 'written to db':
            if about_vacancy['profession']:
                profession = about_vacancy['profession']
                prof_str = ", ".join(profession['profession'])
                additional_message = f"<b>+w: {prof_str}</b>\n{vacancy_url}\n{profession['tag']}\n{profession['anti_tag']}\n\n"
                self.written_vacancies += 1
            else:
                additional_message = 'written to db'
                self.written_vacancies += 1
        if self.bot_dict and self.helper:
            if len(f"{self.current_message}\n{self.count_message_in_one_channel}. {vacancy}\n{additional_message}") < 4096:
                new_text = f"\n{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"
                self.current_message = await self.helper.edit_message(bot=self.bot, text=new_text,
                    msg=self.current_message)
            else:
                new_text = f"{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"
                self.current_message = await self.helper.send_message(bot=self.bot, chat_id=self.chat_id, text=new_text)
        self.count_message_in_one_channel += 1
