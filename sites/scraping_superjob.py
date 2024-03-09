import re
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from db_operations.scraping_db import DataBaseOperations
# from __backup__.pattern_Alex2809 import params
from helper_functions.parser_find_add_parameters.parser_find_add_parameters import FinderAddParameters
from sites.write_each_vacancy_to_db import HelperSite_Parser
from settings.browser_settings import options, chrome_driver_path
from sites.sites_additional_utils.get_structure import get_structure
from utils.additional_variables.additional_variables import sites_search_words, parsing_report_path, admin_database, \
    archive_database
from helper_functions.helper_functions import edit_message, send_message, send_file_to_user
from patterns.data_pattern._data_pattern import cities_pattern, params
from report.report_variables import report_file_path
from helper_functions import helper_functions as helper


class SuperJobGetInformation:

    def __init__(self, **kwargs):

        self.report = kwargs['report'] if 'report' in kwargs else None
        self.search_words = kwargs['search_word'] if 'search_word' in kwargs else sites_search_words
        self.bot_dict = kwargs['bot_dict'] if 'bot_dict' in kwargs else None
        self.helper_parser_site = HelperSite_Parser(report=self.report)
        self.find_parameters = FinderAddParameters()
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
            self.bot = self.bot_dict['bot']
            self.chat_id = self.bot_dict['chat_id']
        self.browser = None
        self.main_url = 'https://russia.superjob.ru'
        self.count_message_in_one_channel = 1
        self.found_by_link = 0
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
                    path=self.report.keys.report_file_path['parsing'],
                )
            except Exception as ex:
                print(f"Error: {ex}")
                if self.bot:
                    await self.bot.send_message(self.chat_id, f"Error: {ex}")
        self.browser.quit()

    async def get_info(self):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # -------------------- check what is current session --------------
        self.current_session = await self.helper_parser_site.get_name_session()

        for word in self.search_words:
            self.word = word
            self.page_number = 0
            till = 13
            for self.page_number in range(1, till):
                try:
                    if self.bot_dict:
                        await self.bot.send_message(self.chat_id,
                                                    f'https://www.superjob.ru/vacancy/search/?keywords={self.word}&remote_work_binary=0&geo%5Bc%5D%5B0%5D=1&noGeo=1&page={self.page_number}',
                                                    disable_web_page_preview=True)
                    self.browser.get(
                        f'https://www.superjob.ru/vacancy/search/?keywords={self.word}&remote_work_binary=0&geo%5Bc%5D%5B0%5D=1&noGeo=1&page={self.page_number}')
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    vacancy_exists_on_page = await self.get_link_message(self.browser.page_source)
                    if not vacancy_exists_on_page:
                        break
                except:
                    break
        if self.bot_dict:
            await self.bot.send_message(self.chat_id, 'superjob.ru parsing: Done!', disable_web_page_preview=True)

    async def get_link_message(self, raw_content):
        soup = BeautifulSoup(raw_content, 'lxml')

        self.list_links = soup.find_all('div', class_='f-test-search-result-item')

        if self.list_links:
            if self.bot_dict:
                self.current_message = await self.bot.send_message(self.chat_id,
                                                                   f'superjob.ru:\nПо слову {self.word} найдено {len(self.list_links)} вакансий на странице {self.page_number}',
                                                                   disable_web_page_preview=True)
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

    async def get_content_from_link(self):
        links = []
        soup = None
        self.found_by_link = 0
        for link in self.list_links:
            found_vacancy = True
            try:
                vacancy_url = link.find('a').get('href')
                vacancy_url = f"{self.main_url}{vacancy_url}"
            except:
                vacancy_url = link
            print(f"\n{vacancy_url}")

            # pre-checking by link
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
                    vacancy = ''
                    try:
                        vacancy = soup.find("h1", class_="_1gB-h h9XuZ _2qyq0 _3t5Je _3TptJ _2C8nO _2L4SY").get_text()
                    except Exception as e:
                        pass

                    salary = ''
                    try:
                        salary = soup.find('span', class_='_2eYAG _3TptJ _2C8nO _3B9u2').get_text()
                    except Exception as e:
                        pass
                    # get title --------------------------
                    title = vacancy

                    # get body --------------------------
                    body = ''
                    body_content = ''
                    try:
                        body = 'Описание вакансии:\n'
                        body_content = soup.find('span', class_='_39I1Z _10jsR _2C8nO _2KJeO _3B9u2 _3nGEP').find(
                            'span')
                    except Exception as e:
                        pass

                    if body_content:
                        structure = await get_structure(body_content)
                        body_content_list_p = body_content.find_all('p')
                        body_content_list_ul = body_content.find_all('ul')
                        for element in structure:
                            if element == 'p':
                                try:
                                    temp = body_content_list_p[0].get_text()
                                    body += f"\n{temp}\n"
                                    # print('\n', temp)
                                    body_content_list_p.pop(0)
                                except:
                                    break
                            if element == 'ul':
                                if body_content_list_ul:
                                    temp = body_content_list_ul[0]
                                    for li in temp:
                                        if li.text != ' ' and li.text:
                                            try:
                                                body += f"-{li.get_text()}\n"
                                                # print('-', li.get_text())
                                            except:
                                                break
                                    body_content_list_ul.pop(0)

                    # get tags --------------------------
                    tags = ''
                    try:
                        tags_list = soup.find('div', class_='_2Qxci').find_all('span', role='button')
                        for i in tags_list:
                            tags += f'{i.get_text()}, '
                        tags = tags[0:-2]
                    except:
                        pass
                    body = f"{body}\nПрофессиональные навыки:\n{tags}"

                    content = ''
                    try:
                        content = soup.find('div', class_='_17PZ- f-test-vacancy-base-info _2FhvV h9XuZ _1MEwQ _3t5Je '
                                                          '_3Fd3- _3m_sI _34KJO _3sU4J')
                    except Exception as e:
                        pass

                    job_type = ''
                    salary = ''
                    city = ''
                    experience = ''
                    if content:
                        try:
                            salary = content.find('span', class_='_2eYAG _3TptJ _2C8nO _3B9u2').get_text()
                            salary = self.find_parameters.salary_to_set_form(text=salary)
                            if salary[0]:
                                salary = ", ".join(salary)
                        except:
                            pass
                        experience_list = content.find_all('span', class_='_1n5Yy _2C8nO _3B9u2')
                        for element in experience_list:
                            if 'пыт работы' in element.text or 'занятость' in element.text:
                                experience += f"{element.text}, "
                        if experience:
                            job_type = experience[:-2]

                        try:
                            city = content.find('span', class_='_1n5Yy _2C8nO _3B9u2').get_text()
                        except:
                            pass

                    english = ''
                    if re.findall(r'[Аа]нглийский', tags) or re.findall(r'[Ee]nglish', tags):
                        english = 'English'

                    # if vacancy and not salary:
                    #     salary = re.findall(fr"[0-9\s,\-\—]{4,}", vacancy)[-1]
                    #     if salary:
                    #         salary = salary + vacancy.split(salary)[-1]
                    # print(salary)
                    # pass

                    # get city --------------------------
                    # try:
                    #     city = soup.find('a', class_='bloko-link bloko-link_kind-tertiary bloko-link_disable-visited').get_text()
                    # except:
                    #     city = ''
                    # print('city = ',city)

                    # get company --------------------------
                    company = ''
                    try:
                        company = soup.find('div',
                                            class_='Fyyve _1MxfQ _2ZP2D').find('span', class_='_3TptJ _2C8nO _2KJeO '
                                                                                              '_3B9u2').get_text()
                    except:
                        company = ''

                    contacts = ''

                    try:
                        date = soup.find_all('span', class_="_10jsR _2C8nO _1Yc2K _3B9u2")[1].get_text()
                    except:
                        date = ''

                    if date:
                        date = self.normalize_date(date)
                    else:
                        date = datetime.now()

                    # ------------------------- search relocation ----------------------------
                    relocation = ''
                    if re.findall(r'[Рр]елокация', body):
                        relocation = 'релокация'

                    # ------------------------- search city ----------------------------
                    # for key in cities_pattern:
                    #     for item in cities_pattern[key]:
                    #         match = re.findall(rf"{item}", body)
                    #         if match and key != 'others':
                    #             for i in match:
                    #                 city += f"{i} "

                    # ------------------------- search english ----------------------------
                    english_additional = ''
                    for item in params['english_level']:
                        match1 = re.findall(rf"{item}", body)
                        match2 = re.findall(rf"{item}", tags)
                        if match1:
                            for i in match1:
                                english_additional += f"{i} "
                        if match2:
                            for i in match2:
                                english_additional += f"{i} "

                    if english and (
                            'upper' in english_additional or 'b1' in english_additional or 'b2' in english_additional
                            or 'internediate' in english_additional or 'pre' in english_additional):
                        english = english_additional
                    elif not english and english_additional:
                        english = english_additional

                    self.db.write_to_db_companies([company])

                    # -------------------- compose one writting for ione vacancy ----------------

                    results_dict = {
                        'chat_name': 'https://superjob.ru/',
                        'title': title,
                        'body': body,
                        'vacancy': vacancy,
                        'vacancy_url': vacancy_url,
                        'company': company,
                        'company_link': '',
                        'english': english,
                        'relocation': relocation,
                        'job_type': job_type,
                        'city': city,
                        'salary': salary,
                        'experience': '',
                        'time_of_public': date,
                        'contacts': contacts,
                        'session': self.current_session
                    }

                    response = await self.helper_parser_site.write_each_vacancy(results_dict)

                    await self.output_logs(
                        about_vacancy=response,
                        vacancy=vacancy,
                        vacancy_url=vacancy_url
                    )
                    self.response = response
            else:
                self.found_by_link += 1
                print("vacancy link exists")

        if self.found_by_link > 0:
            self.count_message_in_one_channel += self.found_by_link
            if self.bot_dict:
                self.current_message = await edit_message(
                    bot=self.bot,
                    text=f"\n---\nfound by link: {self.found_by_link}",
                    msg=self.current_message
                )

    async def get_content_from_one_link(self, vacancy_url):
        try:
            self.browser = webdriver.Chrome(
                executable_path=chrome_driver_path,
                options=options
            )
        except:
            self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # -------------------- check what is current session --------------
        self.current_session = await self.helper_parser_site.get_name_session()
        self.list_links = [vacancy_url]
        await self.get_content_from_link()
        self.browser.quit()
        return self.response

    async def output_logs(self, about_vacancy, vacancy, vacancy_url=None):
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

        if len(f"{self.current_message}\n{self.count_message_in_one_channel}. {vacancy}\n{additional_message}") < 4096:
            new_text = f"\n{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"

            if self.bot_dict:
                self.current_message = await edit_message(
                    bot=self.bot,
                    text=new_text,
                    msg=self.current_message
                )
        else:
            if self.bot_dict:
                new_text = f"{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"
                self.current_message = await send_message(
                    bot=self.bot,
                    chat_id=self.chat_id,
                    text=new_text
                )

        # print(f"\n{self.count_message_in_one_channel} from_channel remote-job.ru search {self.word}")
        self.count_message_in_one_channel += 1

    def normalize_date(self, date):
        date_today = datetime.now().strftime('%d')
        month = datetime.now().strftime('%m')
        year = datetime.now().strftime('%Y')
        hour = datetime.now().strftime('%H')
        minutes = datetime.now().strftime('%M')

        if ':' in date:
            date = date.split(':')
            hour = date[0]
            minutes = date[1]
        if 'вчера' in date:
            date_today = int(date_today) - 1
            hour = 12
            minutes = 00

        date = datetime(int(year), int(month), int(date_today), int(hour), int(minutes), 00)

        return date

    def clean_company_name(self, text):
        text = re.sub('Прямой работодатель', '', text)
        text = re.sub(r'[(]{1} [a-zA-Z0-9\W\.]{1,30} [)]{1}', '', text)
        text = re.sub(r'Аккаунт зарегистрирован с (публичной почты|email) \*@[a-z.]*[, не email компании!]{0,1}', '',
                      text)
        text = text.replace(f'\n', '')
        return text

    async def write_to_db_table_companies(self):
        excel_data_df = pd.read_excel('all_geek.xlsx', sheet_name='Sheet1')
        companies = excel_data_df['hiring'].tolist()
        links = excel_data_df['access_hash'].tolist()

        companies = set(companies)

        self.db.write_to_db_companies(companies)
