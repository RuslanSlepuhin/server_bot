import re
import time
from datetime import datetime, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from db_operations.scraping_db import DataBaseOperations
from sites.write_each_vacancy_to_db import write_each_vacancy
from settings.browser_settings import options, chrome_driver_path
from utils.additional_variables.additional_variables import sites_search_words
from helper_functions.helper_functions import edit_message, send_message


class RemotehubGetInformation:

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
            self.search_words = [search_word]
        self.page_number = 1

        self.current_message = None
        self.msg = None
        self.written_vacancies = 0
        self.rejected_vacancies = 0
        if bot_dict:
            self.bot = bot_dict['bot']
            self.chat_id = bot_dict['chat_id']
        self.browser = None
        self.main_url = 'https://remotehub.com'

    async def get_content(self, db_tables=None):
        """
        If DB_tables = 'all', that it will push to all DB include professions.
        If None (default), that will push in all_messages only
        :param count_message_in_one_channel:
        :param db_tables:
        :return:
        """
        # self.browser.delete_all_cookies()
        # print('all cookies have deleted')
        self.db_tables = db_tables

        self.count_message_in_one_channel = 1

        await self.get_info()

    async def get_info(self):
        self.browser = webdriver.Chrome(
            executable_path=chrome_driver_path,
            options=options
        )
        # self.browser = webdriver.Chrome(
        #     executable_path=chrome_driver_path,
        #     options=options
        # )
        # try:
        await self.bot.send_message(self.chat_id, f'https://www.remotehub.com/jobs/search?sort_type=2',
                                    disable_web_page_preview=True)
        self.browser.get(f'https://www.remotehub.com/jobs/search?sort_type=2')
        # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        till = 0
        while till <= 10:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            till += 1
        vacancy_exists_on_page = await self.get_link_message(self.browser.page_source)
            # if not vacancy_exists_on_page:
            #     break
        # except:
            # break
        await self.bot.send_message(self.chat_id, 'remotehub.com parsing: Done!', disable_web_page_preview=True)
        self.browser.quit()

    async def get_link_message(self, raw_content):

        links = []
        soup = BeautifulSoup(raw_content, 'lxml')

        list_links = soup.find_all('smp-landings-entity', class_='ng-star-inserted')
        if list_links:
            print(f'\nНайдено {len(list_links)} вакансий\n')
            self.current_message = await self.bot.send_message(self.chat_id,
                                                               f'remotehub.com:\nНайдено {len(list_links)} вакансий',
                                                               disable_web_page_preview=True)

            # -------------------- check what is current session --------------

            current_session = DataBaseOperations(None).get_all_from_db(
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
                await self.get_content_from_link(i, links)

            # ----------------------- the statistics output ---------------------------
            self.written_vacancies = 0
            self.rejected_vacancies = 0
            return True
        else:
            return False

    def convert_date(self, date):
        if date == 'Today':
            date = datetime.now()
        else:
            date = datetime.now() - timedelta(days=int(date))
        return date

    def clean_company_name(self, text):
        text = re.sub('Прямой работодатель', '', text)
        text = re.sub(r'[(]{1} [a-zA-Z0-9\W\.]{1,30} [)]{1}', '', text)
        text = re.sub(r'Аккаунт зарегистрирован с (публичной почты|email) \*@[a-z.]*[, не email компании!]{0,1}', '',
                      text)
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

        db = DataBaseOperations(con=None)
        db.write_to_db_companies(companies)

    async def get_content_from_link(self, i, links):
        vacancy_url = i.find('a', class_='entity-detailed-link').get('href')
        vacancy_url = self.main_url + vacancy_url
        print('vacancy_url = ', vacancy_url)
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
        vacancy = soup.find('h1', class_='title mat-headline').text
        print('vacancy = ', vacancy)

        # get title --------------------------
        title = vacancy
        print('title = ', title)

        # get body --------------------------
        body = soup.find('span', class_='mat-subheading-2').text
        body = body.replace('\n\n', '\n')
        body = re.sub(r'\<[A-Za-z\/=\"\-\>\s\._\<]{1,}\>', " ", body)
        print('body = ', body)

        # get tags --------------------------
        level = ''
        # try:
        #     level = soup.find('div', class_='category').get_text()
        # except:
        #     pass

        tags = ''
        try:
            raw_tags = soup.find_all('span', class_="truncate muted-2")
            tags = ''
            for tag in raw_tags:
                tags += tag.text
        except:
            pass
        print('tags = ', tags)

        english = ''
        if re.findall(r'[Аа]нглийский', tags) or re.findall(r'[Ee]nglish', tags):
            english = 'English'

        # get city --------------------------
        try:
            city = soup.find('span', class_='mat-body-2 text').text
        except:
            city = ''
        print('city = ', city)

        # get company --------------------------
        try:
            company = soup.find('div', class_='account-name mat-body-2').text
            # company = company.replace('\xa0', ' ')
            # if 'Прямой работодатель ' in company:
            #     company = company.replace('Прямой работодатель ', '')
            # company = company.replace('\n', ' ')

        except:
            company = ''
        print('company = ', company)

        # get salary --------------------------
        try:
            salary = soup.find('div', class_='price ng-star-inserted')
            if not salary:
                salary = soup.find('span', class_='label muted ng-star-inserted')
            salary = salary.text
        except:
            salary = ''
        print('salary = ', salary)

        # get experience --------------------------
        raw_job_format = soup.find_all('a', class_="ng-star-inserted")
        job_format = ''
        for format in raw_job_format:
            format = format.find('mat-basic-chip')
            if format:
                job_format += format.text
        # try:
        #     experience = soup.find('p', class_='vacancy-description-list-item').find('span').get_text()
        # except:
        #     experience = ''
        # print('experience = ',experience)

        print('job_format = ', job_format)

        contacts = ''

        try:
            date = soup.find('div', class_="mat-body-2 posted-ago muted-2").text.split()[0]
        except:
            date = ''
        if date:
            date = self.convert_date(date)
        print('date = ', date)

        # ------------------------- search relocation ----------------------------
        relocation = ''
        if re.findall(r'[Rr]elocation', body):
            relocation = 'релокация'

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

        DataBaseOperations(None).write_to_db_companies([company])

        # -------------------- compose one writting for ione vacancy ----------------

        results_dict = {
            'chat_name': 'https://remotehub.com/',
            'title': title,
            'body': body,
            'vacancy': vacancy,
            'vacancy_url': vacancy_url,
            'company': company,
            'company_link': '',
            'english': english,
            'relocation': relocation,
            'job_type': job_format,
            'city': city,
            'salary': salary,
            'experience': '',
            'time_of_public': date,
            'contacts': contacts,
            'session': self.current_session
        }

        response_from_db = write_each_vacancy(results_dict)

        await self.output_logs(
            response_from_db=response_from_db,
            vacancy=vacancy,
            vacancy_url=vacancy_url
        )

    async def output_logs(self, response_from_db, vacancy, word=None, vacancy_url=None):

        additional_message = ''
        profession = response_from_db['profession']
        response_from_db = response_from_db['response_from_db']

        if response_from_db:
            additional_message = f'-exists in db\n'
            self.rejected_vacancies += 1

        elif not response_from_db:
            prof_str = ", ".join(profession['profession'])
            additional_message = f"<b>+w: {prof_str}</b>\n{vacancy_url}\n{profession['tag']}\n{profession['anti_tag']}\n"

            if 'no_sort' not in profession['profession']:
                self.written_vacancies += 1
            else:
                self.written_vacancies += 1

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

            # self.current_message = await self.bot.send_message(self.chat_id,
            #                                                    f"{self.count_message_in_one_channel}. {vacancy}\n{additional_message}")

        print(f"\n{self.count_message_in_one_channel} from_channel remotehub.com search {word}")
        self.count_message_in_one_channel += 1

# loop = asyncio.new_event_loop()
# loop.run_until_complete(HHGetInformation(bot_dict={}).get_content())
