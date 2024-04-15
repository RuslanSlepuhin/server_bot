import asyncio
import re
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from db_operations.scraping_db import DataBaseOperations
from utils.additional_variables.additional_variables import vacancies_database
from sites.write_each_vacancy_to_db import HelperSite_Parser
from settings.browser_settings import options, chrome_driver_path
from utils.additional_variables.additional_variables import sites_search_words, how_much_pages, parsing_report_path, admin_database, archive_database
from helper_functions.helper_functions import edit_message, send_message, send_file_to_user
from helper_functions.parser_find_add_parameters.parser_find_add_parameters import FinderAddParameters
from helper_functions import helper_functions as helper
from report.report_variables import report_file_path


def format_body_text(body_content:BeautifulSoup) -> str:
    """ Makes the vacancy body text more readable """
    body_text = body_content.get_text(separator="<>")
    body_text = (body_text
                 .replace("<> <> <> <>", "\n")
                 .replace("<> <> <>", "\n")
                 .replace("<> <>", "\n")
                 .replace("<>", "")
                 .replace("!", "! ")
                 .replace(".•", ".\n•")
                 .replace(";•", ".\n•")
                 .replace(".", ". ")
                 .replace("\u202f", " ")
                 .replace("\u20bd", "р")
                 )
    body_text = re.sub("[\n]{3,}", "\n\n", body_text)
    return body_text

class HHGetInformation:

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
        if self.bot_dict:
            self.bot = self.bot_dict['bot']
            self.chat_id = self.bot_dict['chat_id']
        else:
            self.bot = None
        self.browser = None
        self.find_parameters = FinderAddParameters()
        self.count_message_in_one_channel = 1
        self.found_by_link = 0
        self.response = {}
        self.helper = helper
        self.list_links = []
        self.searching_text_separator = None
        self.base_url = "https://hh.ru"
        self.debug = False
        self.additional = (f"/search/vacancy?"
                           f"search_field=name&"       # Искать совпадениев названии вакансии
                           f"enable_snippets=true&"    # с ревью вакансий в поисковой выдаче
                           f"ored_clusters=true&"      # 
                           f"search_period=3&"         # за последние 3 дня
                           f"text=**word&"             # по ключевому слову
                           f"page=**page"              # номер страницы
                           )
        self.main_class = kwargs['main_class']
        self.source_title_name = "https://hh.ru"
        self.source_short_name = "HH"

        self.links_in_past = []
        self.links_x_path = ["//h2[@class='bloko-header-section-2']/span/a", "//h3[@class='bloko-header-section-3']/span/span/a"]

    async def get_content(self, *args, **kwargs):
        self.words_pattern = kwargs['words_pattern']
        self.db_tables = kwargs['db_tables'] if kwargs.get('db_tables') else vacancies_database
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

    async def get_browser(self):
        try:
            self.browser = webdriver.Chrome(
                executable_path=chrome_driver_path,
                options=options
            )
        except:
            self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    async def get_info(self, how_much_pages=4, separator="+"):
        separator = separator if not self.searching_text_separator else self.searching_text_separator
        await self.get_browser()

        self.words_pattern = [self.words_pattern] if type(self.words_pattern) is str else self.words_pattern
        for word in self.words_pattern:
            self.word = separator.join(word.split(" "))

            # not remote
            for self.page_number in range(0, how_much_pages - 1):
                url = f'{self.base_url}{self.additional.replace("**word", self.word).replace("**page", str(self.page_number))}'
                updated_url = url.replace("search_period=3&", "search_period=3&industry=7&")
                if self.debug:
                    await self.main_class.bot.send_message(self.chat_id, f"Url: {url}",
                                                         disable_web_page_preview=True)
                if not self.page_number:
                    self.browser.get(url)
                    await asyncio.sleep(2)
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.browser.get(updated_url)
                await asyncio.sleep(2)
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                vacancy_exists_on_page = await self.get_link_message(self.browser.page_source)
                if not vacancy_exists_on_page:
                    break

        if self.bot_dict:
            await self.bot.send_message(self.chat_id, f'{self.source_title_name} parsing: Done!',
                                        disable_web_page_preview=True)

    async def get_link_message(self, raw_content):

        def get_links() -> list:
            """
            Retrieves the list of all the links in found vacancies webpage.
            Waits until all the items in the list have been found.
            """
            all_links = []
            for link_x_path in self.links_x_path:
                try:
                    all_links = WebDriverWait(self.browser, 10).until(
                        ec.presence_of_all_elements_located((By.XPATH, link_x_path)))
                except Exception as ex:
                    print(ex)
                if all_links:
                    print("XPATH: ", link_x_path)
                    break
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
            self.list_links.append(link.get_attribute('href'))
        if self.list_links:
            if self.bot_dict:
                self.current_message = await self.bot.send_message(self.chat_id, f'{self.source_short_name}:\nПо слову {self.word} найдено {len(self.list_links)} вакансий на странице {self.page_number+1}', disable_web_page_preview=True)

            # --------------------- LOOP -------------------------
            self.written_vacancies = 0
            self.rejected_vacancies = 0

            await self.get_content_from_link()
            #----------------------- the statistics output ---------------------------
            self.written_vacancies = 0
            self.rejected_vacancies = 0
            return True
        else:
            return False

    async def get_content_from_link(self, return_raw_dictionary=False):
        self.found_by_link = 0
        for link in self.list_links:
            try:
                vacancy_url = link.get('href')
            except:
                vacancy_url = link
            print('url', vacancy_url)
            # pre-checking by link
            check_vacancy_not_exists = self.db.check_exists_message_by_link_or_url(
                vacancy_url=vacancy_url,
                table_list=[admin_database, archive_database]
            )
            if (check_vacancy_not_exists or not check_vacancy_not_exists and return_raw_dictionary) and vacancy_url not in self.links_in_past:
                self.links_in_past.append(vacancy_url)
                try:
                    await self.get_vacancy_data(vacancy_url, return_raw_dictionary)
                except Exception as ex:
                    print(ex)
                    pass
            else:
                self.found_by_link += 1
                print("vacancy link exists")

            # if self.found_by_link > 0:
            #     self.count_message_in_one_channel += self.found_by_link
            #     if self.bot_dict:
            #         self.current_message = await edit_message(
            #             bot=self.bot,
            #             text=f"\n---\nfound by link: {self.found_by_link}",
            #             msg=self.current_message
            #         )

    async def get_vacancy_data(self, vacancy_url, return_raw_dictionary):
                self.browser.get(vacancy_url)
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                vacancy = ''
                try:
                    vacancy = self.browser.find_elements(By.XPATH, "//div[@class='vacancy-title']")[0]
                    vacancy = vacancy.text.split("\n")[0]
                except Exception as e:
                    print(f"error vacancy: {e}")

                if vacancy:
                    company_link = ""
                    title = ''
                    try:
                        title = vacancy
                    except Exception as e:
                        print(f"error title: {e}")

                    body = ''
                    try:
                        body = soup.find('div', class_='vacancy-section')
                        body = format_body_text(body)
                        body = re.sub(r'\<[A-Za-z\/=\"\-\>\s\._\<]{1,}\>', " ", body)
                    except Exception as e:
                        print(f"error body: {e}")

                    if body:
                        tags = ''
                        try:
                            tags_list = soup.find('div', class_="bloko-tag-list")
                            for i in tags_list:
                                tags += f'{i.get_text()}, '
                            tags = tags[0:-2]
                        except Exception as e:
                            print(f"error tags: {e}")

                        english = ''
                        if re.findall(r'[Аа]нглийский', tags) or re.findall(r'[Ee]nglish', tags):
                            english = 'English'

                        try:
                            company = soup.find('span', class_='vacancy-company-name').get_text()
                            company = company.replace('\xa0', ' ')
                            if company:
                                self.db.write_to_db_companies([company])
                        except Exception as e:
                            print(f"error company: {e}")
                            company = ''

                        try:
                            salary = soup.find('div', attrs={'data-qa': 'vacancy-salary'}).get_text()
                        except Exception as e:
                            print(f"error salary: {e}")
                            salary = ''

                        try:
                            experience = soup.find('p', class_='vacancy-description-list-item').find('span').get_text()
                        except Exception as e:
                            print(f"error experience: {e}")
                            experience = ''

                        raw_content_2 = soup.findAll('p', class_='vacancy-description-list-item')
                        counter = 1
                        job_type = ''
                        try:
                            for value in raw_content_2:
                                match counter:
                                    case 1:
                                        experience = value.find('span').get_text()
                                    case 2:
                                        job_type = str(value.get_text())
                                    case 3:
                                        job_type += f'\n{value.get_text}'
                                counter += 1
                            job_type = re.sub(r'\<[a-zA-Z\s\.\-\'"=!\<_\/]+\>', " ", job_type)
                        except Exception as ex:
                            print(ex)
                            pass

                        contacts = ''

                        try:
                            date = soup.find('p', class_="vacancy-creation-time-redesigned").get_text()
                        except Exception as e:
                            print(f"error date: {e}")
                            date = ''
                        if date:
                            try:
                                date = re.findall(r'[0-9]{1,2}\W[а-я]{3,}\W[0-9]{4}', date)
                                date = date[0]
                                date = self.normalize_date(date)
                            except Exception as ex:
                                print(ex)
                                pass

                        # ------------------------- search relocation ----------------------------
                        relocation = ''
                        if re.findall(r'[Рр]елокация', body):
                            relocation = 'релокация'

                        # ------------------------- search city ----------------------------
                        try:
                            city = soup.find('a',
                                             class_='bloko-link bloko-link_kind-tertiary bloko-link_disable-visited').text
                        except:
                            try:
                                city = self.browser.find_elements(By.XPATH, "//p[@data-qa='vacancy-view-location']")[0].text
                            except:
                                city = ''

                        try:
                            await self.collect_result_dict(
                            title, body, vacancy, vacancy_url, company, company_link, english, relocation, job_type,
                            city, salary, experience, date, contacts, return_raw_dictionary, vacancy=vacancy)
                        except Exception as ex:
                            print(ex)
                            pass
                    else:
                        self.response = {}
                else:
                    self.response = {}

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
                    print(ex)
                    pass
                try:
                    print('sort profession (33)')
                    await self.output_logs(
                        about_vacancy=response,
                        vacancy=kwargs['vacancy'],
                        vacancy_url=args[3]
                    )
                    # return response
                    self.response = response
                except Exception as ex:
                    print(ex)
                    pass
            else:
                self.response = results_dict

    async def get_content_from_one_link(self, vacancy_url, return_raw_dictionary=False):
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
        await self.get_content_from_link(return_raw_dictionary)
        self.browser.quit()
        return self.response

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

    def normalize_date(self, date):
        convert = {
            'января': '01',
            'февраля': '02',
            'марта': '03',
            'апреля': '04',
            'мая': '05',
            'июня': '06',
            'июля': '07',
            'августа': '08',
            'сентября': '09',
            'октября': '10',
            'ноября': '11',
            'декабря': '12',
        }

        date = date.split(f'\xa0')
        month = date[1]
        day = date[0]
        year = date[2]

        date = datetime(int(year), int(convert[month]), int(day), 12, 00, 00)

        return date

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

    async def one_url(self, url):
        self.list_links = [url]
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        await self.get_content_from_link()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(HHGetInformation(bot_dict={}).get_content())


