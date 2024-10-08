import re
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from db_operations.scraping_db import DataBaseOperations
from sites.write_each_vacancy_to_db import write_each_vacancy
from settings.browser_settings import options, chrome_driver_path
from utils.additional_variables.additional_variables import sites_search_words, how_much_pages
from helper_functions.helper_functions import edit_message, send_message
from sites.send_log_txt import send_log_txt
from helper_functions import helper_functions as helper

class GorodRabotGetInformation:

    def __init__(self, bot_dict, search_word=None):

        self.db_tables = None
        self.options = None
        self.page = None
        self.to_write_excel_dict = {
            'chat_name': [],
            'title': [],
            'body': [],
            'vacancy': [],
            'vacancy_url': [],
            'company': [],
            'company_link': [],
            'english': [],
            'relocation': [],
            'job_type': [],
            'city': [],
            'salary': [],
            'experience': [],
            'time_of_public': [],
            'contacts': []
        }
        if not search_word:
            self.search_words = sites_search_words
        else:
            self.search_words=[search_word]
        self.page_number = 1
        self.current_message = None
        self.msg = None
        self.written_vacancies = 0
        self.rejected_vacancies = 0
        if bot_dict:
            self.bot = bot_dict['bot']
            self.chat_id = bot_dict['chat_id']
        self.browser = None
        self.count_message_in_one_channel = 1
        self.helper = helper


    async def get_content(self, db_tables=None):
        self.db_tables = db_tables

        self.count_message_in_one_channel = 1

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
        for word in self.search_words:
            while True:
                try:
                    await self.bot.send_message(self.chat_id, f"https://belarus.gorodrabot.by/?q={word}&d=%D0%B7%D0%B0+%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%B8%D0%B9+%D0%B4%D0%B5%D0%BD%D1%8C&p={self.page_number}")
                    self.browser.get(f"https://belarus.gorodrabot.by/?q={word}&d=%D0%B7%D0%B0+%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%D0%B4%D0%BD%D0%B8%D0%B9+%D0%B4%D0%B5%D0%BD%D1%8C&p={self.page_number}")
                    # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    vacancy_exists_on_page = await self.get_link_message(self.browser.page_source, word)
                    if not vacancy_exists_on_page:
                        break
                except:
                    break
                self.page_number += 1

        await self.bot.send_message(self.chat_id, 'gorodrabot.by parsing: Done!', disable_web_page_preview=True)

    async def get_link_message(self, raw_content, word):

        links = []
        soup = BeautifulSoup(raw_content, 'lxml')
        vacancies_list = soup.find_all('div', class_='result-list__snippet')[:-1]
        list_links = []
        for vacancy in vacancies_list:
            rabotaby = vacancy.text.split()
            rabotaby = ' '.join(rabotaby)
            if 'rabota.by' in rabotaby:
                continue
            v = vacancy.find('a', class_='snippet__title-link link an-vc')
            list_links.append(v)

        if list_links:
            print(f'\nПо слову {word} найдено {len(list_links)} вакансий\n')
            self.current_message = await self.bot.send_message(self.chat_id, f'gorodrabot.by:\nПо слову {word} найдено {len(list_links)} вакансий на странице {self.page_number+1}', disable_web_page_preview=True)

            # -------------------- check what is current session --------------

            current_session = DataBaseOperations().get_all_from_db(
                table_name='current_session',
                param='ORDER BY id DESC LIMIT 1',
                without_sort=True,
                order=None,
                field='session',
                curs=None
            )
            for value in current_session:
                self.current_session = value[0]

            # --------------------- LOOP -------------------------
            self.written_vacancies = 0
            self.rejected_vacancies = 0

            for i in list_links:
                await self.get_content_from_link(i, links, word)

            #----------------------- the statistics output ---------------------------
            self.written_vacancies = 0
            self.rejected_vacancies = 0
            return True
        else:
            return False


    def clean_company_name(self, text):
        text = re.sub('Прямой работодатель', '', text)
        text = re.sub(r'[(]{1} [a-zA-Z0-9\W\.]{1,30} [)]{1}', '', text)
        text = re.sub(r'Аккаунт зарегистрирован с (публичной почты|email) \*@[a-z.]*[, не email компании!]{0,1}', '', text)
        text = text.replace(f'\n', '')
        return text

    async def compose_in_one_file(self):
        hiring = []
        link = []
        contacts = []

        for i in range(1, 48):
            excel_data_df = pd.read_excel(f'./../messages/geek{i}.xlsx', sheet_name='Sheet1')

            hiring.extend(excel_data_df['hiring'].tolist())
            link.extend(excel_data_df['hiring_link'].tolist())
            contacts.extend(excel_data_df['contacts'].tolist())

        df = pd.DataFrame(
            {
            'hiring': hiring,
            'access_hash': link,
            'contacts': contacts,
            }
        )

        df.to_excel(f'all_geek.xlsx', sheet_name='Sheet1')

    async def write_to_db_table_companies(self):
        excel_data_df = pd.read_excel('all_geek.xlsx', sheet_name='Sheet1')
        companies = excel_data_df['hiring'].tolist()
        links = excel_data_df['access_hash'].tolist()

        companies = set(companies)

        db=DataBaseOperations(con=None)
        db.write_to_db_companies(companies)

    async def get_content_from_link(self, i, links, word):
        try:
            vacancy_url = i.get('href')
            # vacancy_url = re.findall(r'https:\/\/hh.ru\/vacancy\/[0-9]{6,12}', vacancy_url)[0]
            # print('vacancy_url = ', vacancy_url)
        except:
            vacancy_url = i
        links.append(vacancy_url)

        print('self.broswer.get(vacancy_url)')
        # await self.bot.send_message(self.chat_id, vacancy_url, disable_web_page_preview=True)
        # self.browser = browser
        self.browser.get(vacancy_url)
        # self.browser.get('https://google.com')
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        print('soup = BeautifulSoup(self.browser.page_source, \'lxml\')')
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        print('passed soup = BeautifulSoup(self.browser.page_source, \'lxml\')')

        # get vacancy ------------------------
        vacancy = soup.find('h1', class_='vacancy-view__title content__title').text
        vacancy = vacancy.split()[2:-2]
        vacancy = ' '.join(vacancy)
        print('vacancy = ', vacancy)

        # get title --------------------------
        title = vacancy
        print('title = ',title)

        # get body --------------------------
        body = soup.find('div', class_='vacancy-view__body').text.strip()
        body = body.replace('\n\n', '\n')
        body = re.sub(r'\<[A-Za-z\/=\"\-\>\s\._\<]{1,}\>', " ", body)
        print('body = ',body)

        # get tags --------------------------
        tags = ''
        # try:
        #     tags_list = soup.find('div', class_="bloko-tag-list")
        #     for i in tags_list:
        #         tags += f'{i.get_text()}, '
        #     tags = tags[0:-2]
        # except:
        #     pass
        print('tags = ',tags)

        english = ''
        if re.findall(r'[Аа]нглийский', tags) or re.findall(r'[Ee]nglish', tags):
            english = 'English'

        # get city --------------------------
        try:
            city = soup.find_all('a', class_='breadcrumbs__link link')[1].text
        except:
            city = ''
        print('city = ',city)

        # get company --------------------------
        try:
            company = soup.find('div', class_='property fa fa-briefcase').find('span', class_='property__value').text.strip()
        except:
            company = ''
        print('company = ',company)

        # get salary --------------------------
        try:
            salary = soup.find('li', class_='range-list__point').text
            salary = salary.split()
            salary = ' '.join(salary)
        except:
            salary = ''
        print('salary = ',salary)

        # get experience --------------------------
        try:
            experience = soup.find('div', class_='property property_style_big-icon fa fa-shapes').find('span', class_='property__value').text.strip()
        except:
            experience = ''
        print('experience = ',experience)

        # get job type and remote --------------------------
        raw_content_2 = soup.findAll('p', class_='vacancy-description-list-item')
        counter = 1
        try:
            job_type = soup.find('div', class_='property property_style_big-icon fa fa-user-clock').find('span', class_='property__value').text.strip()
        except:
            job_type = ''

        try:
            date = datetime.today()
        except:
            date = ''
        print('date = ', date)

        # ------------------------- search relocation ----------------------------
        relocation = ''
        if re.findall(r'[Рр]елокация', body):
            relocation = 'релокация'

        contacts = ''

        # ------------------------- search city ----------------------------
        # city = ''
        # for key in cities_pattern:
        #     for item in cities_pattern[key]:
        #         match = re.findall(rf"{item}", body)
        #         if match and key != 'others':
        #             for i in match:
        #                 city += f"{i} "

        # ------------------------- search english ----------------------------
        # english_additional = ''
        # for item in params['english_level']:
        #     match1 = re.findall(rf"{item}", body)
        #     match2 = re.findall(rf"{item}", tags)
        #     if match1:
        #         for i in match1:
        #             english_additional += f"{i} "
        #     if match2:
        #         for i in match2:
        #             english_additional += f"{i} "
        #
        # if english and ('upper' in english_additional or 'b1' in english_additional or 'b2' in english_additional \
        #         or 'internediate' in english_additional or 'pre' in english_additional):
        #     english = english_additional
        # elif not english and english_additional:
        #     english = english_additional

        DataBaseOperations().write_to_db_companies([company])

        #-------------------- compose one writting for ione vacancy ----------------

        results_dict = {
            'chat_name': 'https://gorodrabot.by/',
            'title': title,
            'body': body,
            'vacancy': vacancy,
            'vacancy_url': vacancy_url,
            'company': company,
            'company_link': '',
            'english': english,
            'relocation': relocation,
            'job_type': job_type,
            'city':city,
            'salary':salary,
            'experience':experience,
            'time_of_public':date,
            'contacts':contacts,
            'session': self.current_session
        }


        response_from_db = write_each_vacancy(results_dict)

        await self.output_logs(
            response_from_db=response_from_db,
            vacancy=vacancy,
            word=word,
            vacancy_url=vacancy_url
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
        self.list_links= [vacancy_url]
        response = await self.get_content_from_link()
        return response
    async def output_logs(self, response_from_db, vacancy, word=None, vacancy_url=None):

        additional_message = ''
        profession = response_from_db['profession']
        response_from_db = response_from_db['response_from_db']

        if response_from_db:
            additional_message = f'-exists in db\n'
            self.rejected_vacancies += 1

        elif not response_from_db:
            prof_str = ", ".join(profession['profession'])
            additional_message = f"<b>+w: {prof_str}</b>\n{vacancy_url}\n{profession['tag']}\n{profession['anti_tag']}\n-------\n"

            text_for_log = f"{vacancy}\n+w: {prof_str}\n{vacancy_url}\n{profession['tag']}\n{profession['anti_tag']}\n-------\n"
            await send_log_txt(text_for_log)

            # if 'no_sort' not in profession['profession']:
            #     self.written_vacancies += 1
            # else:
            #     self.written_vacancies += 1

        if len(f"{self.current_message}\n{self.count_message_in_one_channel}. {vacancy}\n{additional_message}") < 4096:
            new_text = f"\n{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"

            self.current_message = await edit_message(
                bot=self.bot,
                text=new_text,
                msg=self.current_message
            )

        else:
            new_text = f"{self.count_message_in_one_channel}. {vacancy}\n{additional_message}"
            self.current_message = await send_message(
                bot=self.bot,
                chat_id=self.chat_id,
                text=new_text
            )

        print(f"\n{self.count_message_in_one_channel} from_channel gorodrabot.by search {word}")
        self.count_message_in_one_channel += 1

    async def get_content_by_link_alone(self, link):
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            self.browser.get(link)
        except Exception as e:
            print(e)
            await self.bot.send_message(self.chat_id, str(e))
            return False
        try:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            pass
        self.browser.quit()
