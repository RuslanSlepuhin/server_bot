from db_operations.scraping_db import DataBaseOperations
from filters.filter_jan_2023.filter_jan_2023 import VacancyFilter
from utils.additional_variables.additional_variables import table_list_for_checking_message_in_db as tables

class HelperSite_Parser:
    def __init__(self, **kwargs):
        self.report = kwargs['report'] if 'report' in kwargs else None
        self.db = DataBaseOperations(report=self.report)
        self.filter = VacancyFilter(report=self.report)

    def write_each_vacancy(self, results_dict):
        response = {}
        profession = []
        self.report.parsing_report(
            link_current_vacancy = results_dict['vacancy_url'],
            title = results_dict['title'],
            body = results_dict['body'],
        )

        # exist_or_not = self.db.check_vacancy_exists_in_db(
        #     tables_list=tables,
        #     title=results_dict['title'],
        #     body=results_dict['body']
        # )

        check_vacancy_exists = self.db.check_exists_message_by_link_or_url(
            vacancy_url=results_dict['vacancy_url'],
            table_list=tables
        )

        # if not exist_or_not:
        if check_vacancy_exists:
            profession = self.filter.sort_profession(
                title=results_dict['title'],
                body=results_dict['body'],
                get_params=False,
                check_vacancy=True,
                check_vacancy_only_mex=True,
                check_contacts=False
            )

            profession = profession['profession']
            self.report.parsing_report(ma=profession['tag'], mex=profession['anti_tag'])

            if profession['profession']:
                response_from_db = self.db.push_to_admin_table(
                    results_dict=results_dict,
                    profession=profession,
                    check_or_exists=True
                )
                response['vacancy'] = 'found in db by title-body' if response_from_db else 'written to db'
            else:
                response['vacancy'] = 'no vacancy by anti-tags'
        else:
            response['vacancy'] = 'found in db by link'

        self.report.parsing_switch_next(switch=True)
        return {'response': response, "profession": profession}

        # self.report.parsing_switch_next(switch=True)
        # # return {'response_from_db': exist_or_not, "profession": None}
        # return {'response_from_db': not check_vacancy_exists, "profession": None}

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