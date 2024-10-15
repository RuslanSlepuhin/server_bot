import asyncio
import pandas as pd
import re
import requests

from db_operations.scraping_db import DataBaseOperations
from helper_functions.helper_functions import edit_message, send_message, send_file_to_user
from helper_functions.parser_find_add_parameters.parser_find_add_parameters import FinderAddParameters
from helper_functions import helper_functions as helper
from report.report_variables import report_file_path
from sites.write_each_vacancy_to_db import HelperSite_Parser
from utils.additional_variables.additional_variables import vacancies_database, sites_search_words, how_much_pages, parsing_report_path, admin_database, archive_database


class HHGetInformationAPI:
    """
        Документация по API https://github.com/hhru/api
    """


    def __init__(self, **kwargs):
        self.report = kwargs['report'] if 'report' in kwargs else None
        self.bot_dict = kwargs['bot_dict'] if 'bot_dict' in kwargs else None
        self.helper_parser_site = HelperSite_Parser(report=self.report)
        self.search_words = [kwargs['search_word']] if 'search_word' in kwargs else sites_search_words
        self.db = DataBaseOperations(report=self.report)
        self.db_tables = None
        self.options = None
        self.page = None
        self.page_number = 1
        self.current_message = None
        self.msg = None
        self.written_vacancies = 0
        self.rejected_vacancies = 0
        self.bot = None
        if self.bot_dict:
            self.bot = self.bot_dict['bot']
            self.chat_id = self.bot_dict['chat_id']
        self.browser = None
        self.find_parameters = FinderAddParameters()
        self.count_message_in_one_channel = 1
        self.found_by_link = 0
        self.response = {}
        self.helper = helper
        self.list_links = []
        self.searching_text_separator = None
        self.base_url = "https://api.hh.ru/vacancies"
        self.host = "hh.ru" # можно выбирать один из hh.ru, rabota.by, hh1.az, hh.uz, hh.kz, headhunter.ge, headhunter.kg
        self.debug = True

        self.main_class = kwargs['main_class'] if kwargs.get('main_class') else None
        self.source_title_name = "https://api.hh.ru"
        self.source_short_name = "HH"

        self.links_in_past = []

        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0" # необходимо указать User-Agent, иначе будет ответ с кодом 400


    async def get_content(self, *args, **kwargs) -> bool:
        # await self.report.reset_collect_parser_links()
        self.words_pattern = kwargs['words_pattern']

        self.db_tables = kwargs['db_tables'] if kwargs.get('db_tables') else vacancies_database
        try:
            if not await self.get_info():
                print("GET CONTENT: not get_info()")
                return False
        except Exception as ex:
            print(f"{self.base_url}: get_content -> Error: {ex}")
            if self.bot:
                await self.bot.send_message(self.chat_id, f"Error: {ex}")

        if self.report and self.helper and self.bot and self.chat_id:
            try:
                await self.report.add_to_excel()
                await self.helper.send_file_to_user(
                    bot=self.bot,
                    chat_id=self.chat_id,
                    path=self.report.keys.report_file_path['parsing'],
                )
            except Exception as ex:
                print(f"{self.base_url}: get_content(2) -> Error: {ex}")
                if self.bot:
                    await self.bot.send_message(self.chat_id, f"Error: {ex}")
        return True


    async def get_info(self, how_much_pages=6, separator=" ") -> bool:
        """
            Get all vacancies based on keywords
        """
        separator = separator if not self.searching_text_separator else self.searching_text_separator
        # self.words_pattern = [self.words_pattern] if type(self.words_pattern) is str else self.words_pattern
        self.word = separator.join(self.words_pattern.split(" "))

        url = self.base_url
        params = {
            "text": self.word,
            "per_page": 100,
            "page": 0,
            "host": self.host,
                }
        headers = {
            "User-Agent": self.user_agent
                }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("items", [])
            found_vacancies = data.get("found")
            pages = data.get("pages") # всего страниц по per_page ваканский на странице, ограничение в 2000 вакансий через запросы открытое API
            self.current_message = await self.bot.send_message(self.chat_id, f'{self.source_short_name}:\nПо слову {self.word} найдено {found_vacancies} вакансий на странице {self.page_number+1}', disable_web_page_preview=True)
            # print(response.status_code, found_vacancies)
        else:
            err = response.json().get("errors").get("type")
            print(f"Got error with status code: {response.status_code}, type: {err}")
            await self.bot.send_message(self.chat_id, f"Got error with status code: {response.status_code}, type: {err}")
            return False

        self.list_links = []

        for vacancy in vacancies:
            # url -> "api.hh.ru"
            # alternate_url	-> "hh.ru"
            self.list_links.append(vacancy.get("url"))
        # print(self.list_links)

        if how_much_pages > pages:
            how_much_pages = pages

        for self.page_number in range(1, how_much_pages):
            if self.debug and self.main_class:
                await self.main_class.bot.send_message(self.chat_id, f"Url: {url}",
                                                                    disable_web_page_preview=True)

            params["page"] += 1
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            vacancies = data.get("items", [])

            for vacancy in vacancies:
                self.list_links.append(vacancy.get("url"))

            print(len(self.list_links), self.bot_dict)

            if self.bot_dict: # bot_dict словарь для телеграм бота
                await self.bot.send_message(self.chat_id, f'{self.source_title_name} parsing: Done!',
                                                disable_web_page_preview=True)
            try:
                await self.get_content_from_link()
            except Exception as ex:
                print(f"get_info error {self.base_url}: get_content_from_link (2) -> ", ex)


    async def get_content_from_link(self, return_raw_dictionary=True):
        self.found_by_link = 0
        print(len(self.list_links), len(self.links_in_past))
        for link in self.list_links:
            vacancy_url = link # alternate_url if checking hh.ru
            print(f'{self.base_url}: get_content_from_link -> url', vacancy_url)
            # pre-checking by link
            check_vacancy_not_exists = self.db.check_exists_message_by_link_or_url(
                vacancy_url=vacancy_url,
                table_list=[admin_database, archive_database]
            )
            if vacancy_url not in self.links_in_past and check_vacancy_not_exists:
                self.links_in_past.append(vacancy_url)
                try:
                    # print(vacancy_url)
                    await self.get_vacancy_data(vacancy_url, return_raw_dictionary)
                except Exception as ex:
                    print(f"get_content_from_link error {self.base_url}: get_content_from_link (2) -> ", ex)
            else:
                self.found_by_link += 1
                print(f"{self.base_url}: vacancy link exists")


    async def get_vacancy_data(self, vacancy_url, return_raw_dictionary):
        vacancy_response = requests.get(vacancy_url)

        if vacancy_response.status_code == 200:
            vacancy_json = vacancy_response.json()

            title = vacancy_json["name"] # название вакансии
            body = vacancy_json["description"] # описание вакансии так же в брендированных вакансиях поле branded_description
            body = re.sub(r'\<[A-Za-z\/=\"\-\>\s\._\<]{1,}\>', " ", body) # убирает html из описания вакансии
            vacancy = vacancy_json["professional_roles"][0]["name"] # looking for a specialist
            company = vacancy_json["employer"]["name"] # название компании
            company_link = vacancy_json["employer"]["url"] # alternate_url - ссылка на компанию не из апи
            # languages = vacancy_json["languages"]
            english = ", ".join([f'{x["name"]} - {x["level"]["name"]}' for x in vacancy_json["languages"]]) # выбирает все языки и уровень
            relocation = ''
            if re.findall(r'[Рр]елокация', body):
                relocation = 'релокация'
            job_type = vacancy_json["employment"]["name"] # занятость
            city = vacancy_json["area"]["name"] # город работы
            salary = f'{vacancy_json["salary"]["from"]} - {vacancy_json["salary"]["to"]} {vacancy_json["salary"]["currency"]}'
            experience = vacancy_json["experience"]["name"] # требуемый опыт
            # responsibilities
            contacts = ''
            date = vacancy_json["published_at"][0:10] #'2024-09-05T09:30:36+0300'
            try:
                await self.collect_result_dict(
                title, body, vacancy, vacancy_url, company, company_link, english, relocation, job_type,
                city, salary, experience, date, contacts, return_raw_dictionary, vacancy=vacancy)
            except Exception as ex:
                    print(f"get_vacancy_data error {self.base_url}: get_vacancy_data (2) -> ", ex)
        else:
            print(f"{self.base_url}: get_vacancy_data-> error response: {vacancy_response.status_code}")



    async def collect_result_dict(self, *args, **kwargs):
        results_dict = {
            'chat_name': self.source_title_name,
            'title': args[0],
            'body': args[1],
            'vacancy': args[2],
            'vacancy_url': args[3],
            'company': args[4],
            'company_link': args[5],
            'english': args[6],
            'relocation': args[7],
            'job_type': args[8],
            'city': args[9],
            'salary': args[10],
            'experience': args[11],
            'time_of_public': args[12],
            'contacts': args[13],
        }

        if not args[14]:
            try:
                response = await self.helper_parser_site.write_each_vacancy(results_dict)
            except Exception as ex:
                print(f"{self.base_url}: collect_result_dict (1)", ex)
            try:
                # print('collect_result_dict -> sort profession (33)')
                await self.output_logs(
                    about_vacancy=response,
                    vacancy=kwargs['vacancy'],
                    vacancy_url=args[3]
                )
                # return response
                self.response = response
            except Exception as ex:
                print(f"{self.base_url}: collect_result_dict (2) -> ", ex)
        else:
            self.response = results_dict


    async def output_logs(self, about_vacancy, vacancy, vacancy_url=None):
        additional_message = ''

        if about_vacancy['response']['vacancy'] in ['found in db by link', 'found in db by title-body']:
            additional_message = f'-exists in db\n\n'
            self.rejected_vacancies += 1

        elif about_vacancy['response']['vacancy'] == 'no vacancy by anti-tags':
            additional_message = f"-ANTI-TAG by vacancy:\a{about_vacancy['profession']['anti_tag']}\n\n"
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

        if self.bot_dict:
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

        # print(f"\n{self.count_message_in_one_channel} from_channel remote-job.ru search {self.word}")
        self.count_message_in_one_channel += 1


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

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(HHGetInformationAPI(bot_dict={}).get_content())