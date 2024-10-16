import asyncio
from datetime import datetime
from re import search
# from sites.sites_additional_utils.ask_gemini import ask_gemini
from sites.sites_additional_utils.ask_ai import ask_ai
from db_operations.scraping_db import DataBaseOperations
from filters.filter_jan_2023.filter_jan_2023 import VacancyFilter
from helper_functions.parser_find_add_parameters.parser_find_add_parameters import FinderAddParameters
from sites.sites_additional_utils.ask_gemini import ask_gemini, ask_gemini_free_request
from utils.additional_variables.additional_variables import vacancy_table, reject_table, \
    table_list_for_checking_message_in_db as tables, \
    admin_database, archive_database, admin_table_fields, valid_professions
from helper_functions.helper_functions import get_salary_usd_month, replace_NoneType, get_tags, \
    get_additional_values_fields, compose_simple_list_to_str, compose_to_str_from_list

class HelperSite_Parser:
    def __init__(self, **kwargs):
        self.report = kwargs['report'] if 'report' in kwargs else None
        self.db = DataBaseOperations(report=self.report)
        self.filter = VacancyFilter(report=self.report)
        self.find_parameters = FinderAddParameters()
        self.results_dict = {}
        self.profession = {}
        self.ai_mode = {
            'Gemini': True,
            'Llama': False
        }

    async def write_each_vacancy(self, results_dict):
        self.results_dict = results_dict
        response = {}
        response_from_db = {}

        if self.report:
            self.report.parsing_report(
                link_current_vacancy=self.results_dict['vacancy_url'],
                title=self.results_dict['title'],
                body=self.results_dict['body'],
            )

        check_vacancy_not_exists = True
        has_been_found_by_title_body = False
        # search this vacancy in database
        if 'vacancy_url' in self.results_dict and self.results_dict['vacancy_url']:
            check_vacancy_not_exists = self.db.check_exists_message_by_link_or_url(
                vacancy_url=self.results_dict['vacancy_url'],
                table_list=tables
            )
        if check_vacancy_not_exists:
            has_been_found_by_title_body = self.db.check_vacancy_exists_in_db(
                tables_list=['vacancies', 'admin_last_session', 'archive'],
                title=self.results_dict['title'],
                body=self.results_dict['body']
            )['has_been_found']
        # check weather this is a vacancy and, if so, weather it relates to IT using Gemini
        # ai_prompt = results_dict['title'] + results_dict['body']
        # for question in ["Is IT?"]:
        #     answer = ask_ai(question, ai_prompt)
        #     if search(r"[Нн]е ", answer) or search(r"[Нн]ет", answer):
        #         check_vacancy_not_exists = False
        #         break
        #     if search(r"[Дд]а", answer):
        #         continue
        #     elif answer == "":
        #         continue

        if check_vacancy_not_exists and not has_been_found_by_title_body:
            approved_status = None
            ai_profession = None
            try:
                ai_profession, approved_status = await self.get_ai_profession()
            except Exception as ex:
                print(ex)
                pass

            print(f"\033[1;32mAI profession: {ai_profession}\033[0m")
            # task = asyncio.create_task(self.get_ai_profession())
            # done, pending = await asyncio.wait([task], return_when=asyncio.ALL_COMPLETED)
            # ai_profession = task.result()
            # print(ai_profession)


            # get profession's parameters
            try:
                self.profession = self.filter.sort_profession(
                title=self.results_dict['title'],
                body=self.results_dict['body'],
                get_params=False,
                check_vacancy=True,
                check_vacancy_only_mex=True,
                check_contacts=False,
                vacancy_dict=self.results_dict,
                ai_profession=ai_profession if ai_profession else None
            )
            except Exception as ex:
                print("write_each_vacancy (1) - > ", ex)
                pass

            self.profession = self.profession['profession']
            print(f"\033[1;32mFILTER profession: {', '.join(self.profession['profession'])}\033[0m")


            if self.report:
                self.report.parsing_report(ma=self.profession['tag'], mex=self.profession['anti_tag'])

            # fill all fields
            try:
                await self.fill_all_fields()
            except Exception as ex:
                print("write_each_vacancy (2) - > ", ex)
                pass

            if self.profession['profession']:
                self.results_dict['approved'] = 'approves by filter' if not approved_status else approved_status
                print(f"\033[1;32mAPPROVED: {self.results_dict['approved']}\033[0m")

                try:
                    response_from_db = self.db.push_to_admin_table(
                    results_dict=self.results_dict,
                    profession=self.profession,
                    check_or_exists=True
                    )
                except Exception as ex:
                    print("write_each_vacancy (3) - > ", ex)
                    pass

                if self.report:
                    try:
                        self.report.parsing_report(approved=self.results_dict['approved'])
                    except Exception as ex:
                        print("write_each_vacancy (3) - > ", ex)
                        pass

                if not response_from_db:
                    return False
                response['vacancy'] = 'found in db by title-body' if response_from_db['has_been_found'] else 'written to db'
            else:
                self.results_dict['profession'] = ''

                self.results_dict['approved'] = 'rejects by filter'
                self.db.check_or_create_table(
                    table_name=reject_table,
                    fields=vacancy_table
                )

                try:
                    self.db.push_to_db_common(
                    table_name=reject_table,
                    fields_values_dict=self.results_dict,
                    notification=True
                    )
                except Exception as ex:
                    print("write_each_vacancy (4) - > ", ex)
                    pass

                if self.report:
                    self.report.parsing_report(approved=self.results_dict['approved'])

                response['vacancy'] = 'no vacancy by anti-tags'
        else:
            response['vacancy'] = 'found in db by link' if not check_vacancy_not_exists else 'found in db by title-body'
        if self.report:
            self.report.parsing_switch_next(switch=True)


        return {'response': response, "profession": self.profession, 'response_dict': response_from_db}

    async def get_name_session(self):
        current_session = self.db.get_all_from_db(
            table_name='current_session',
            param='ORDER BY id DESC LIMIT 1',
            without_sort=True,
            order=None,
            field='session',
            curs=None
        )
        for value in current_session:
            current_session = value[0]
        return  current_session

    async def fill_all_fields(self):

        for key in set(self.results_dict.keys()).difference(set(admin_table_fields.split(", "))):
            self.results_dict.pop(key)
        for key in self.results_dict:
            if type(self.results_dict[key]) in (set, list, tuple):
                self.results_dict[key] = ", ".join(self.results_dict[key])

        # refactoring and filling additional vacancy fields
        self.results_dict['tags'] = get_tags(self.profession)
        self.results_dict['full_tags'] = self.profession['tag'].replace("'", "")
        self.results_dict['full_anti_tags'] = self.profession['anti_tag'].replace("'", "")
        self.results_dict['created_at'] = datetime.now()
        self.results_dict['level'] = self.profession['level']
        self.results_dict['company'] = self.db.clear_title_or_body(self.results_dict['company'])
        self.results_dict['profession'] = compose_simple_list_to_str(data_list=self.profession['profession'], separator=', ')
        self.results_dict['sub'] = compose_to_str_from_list(data_list=self.profession['sub'])
        if not self.results_dict['time_of_public']:
            self.results_dict['time_of_public'] = datetime.now()
        self.results_dict = get_additional_values_fields(
            dict_in=self.results_dict
        )
        # salary refactoring
        region = 'BY' if 'praca.by' in self.results_dict['vacancy_url'] else None
        if 'salary' in self.results_dict and self.results_dict['salary']:
            salary = self.find_parameters.salary_to_set_form(text=self.results_dict['salary'], region=region)
            salary = await self.find_parameters.compose_salary_dict_from_salary_list(salary)
            for key in salary:
                self.results_dict[key] = salary[key]
            self.results_dict = await get_salary_usd_month(
                vacancy_dict=self.results_dict
            )
        self.results_dict['job_type'] = await self.find_parameters.get_job_types(self.results_dict)
        self.results_dict = await replace_NoneType(results_dict=self.results_dict)

        # city and country refactoring
        if self.results_dict['city']:
            city_country = await self.find_parameters.find_city_country(text=self.results_dict['city'])
            if city_country:
                self.results_dict['city'] = city_country
            else:
                self.results_dict['city'] = ''

    async def get_ai_profession(self, **kwargs):
        self.results_dict['title'] = kwargs['title'] if kwargs.get('title') else self.results_dict['title']
        self.results_dict['body'] = kwargs['body'] if kwargs.get('body') else self.results_dict['body']
        act_prof = valid_professions.copy()
        act_prof.pop(0)
        request = f"Если это IT вакансия, то определи ее профессию из списка профессий: [{', '.join(act_prof)}]. Вакансия: {self.results_dict['title']}\n{self.results_dict['body']}. Ответ выдай одним словом (конкретной профессией из списка). Если это не IT вакансия или если ни одна профессия из списка не соответствует вакансии, то выдай ответ no_sort"
        answer = ''
        approved_status = None
        status_code = 500
        ai = "Gemini" if self.ai_mode["Gemini"] else "Llama"
        for _ in range(0, len(self.ai_mode)*2):
            answer, status_code, approved_status, ai_name_from = await ask_ai(request, ai)
            if status_code >= 400:
                ai = await self.next_ai(ai)
            else:
                break
        answer = answer.replace("\n", "").strip()
        if 200 <= status_code < 300:
            answer = await self.define_more_precisely(answer)
        if answer and answer not in valid_professions:
            return "", None
        elif answer == "no_sort":
            return "no_sort", approved_status
        else:
            return answer, approved_status

    async def next_ai(self, ai, global_switch=False):
        all_ai = list(self.ai_mode.keys())
        ai_index = all_ai.index(ai)
        if ai_index != len(self.ai_mode)-1:
            self.ai_mode[ai] = False if global_switch else True
            ai = all_ai[ai_index+1]
            self.ai_mode[ai] = True if global_switch else False
        else:
            self.ai_mode[ai] = False if global_switch else True
            ai = all_ai[0]
            self.ai_mode[ai] = True if global_switch else False
        return ai

    async def define_more_precisely(self, answer):
        v_prof = valid_professions.copy()
        v_prof.remove('junior')
        if answer.lower() in v_prof:
            return answer
        answer = self.filter.sort_profession(
            title=answer,
            body="",
            get_params=False,
            check_vacancy=True,
            check_vacancy_only_mex=True,
            check_contacts=False,
            vacancy_dict={'title': answer, "body": None},
        )
        if 'junior' in answer['profession']['profession']:
            answer['profession']['profession'].remove('junior')
        return ", ".join(answer['profession']['profession'])
