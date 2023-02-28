from db_operations.scraping_db import DataBaseOperations
from filters.filter_jan_2023.filter_jan_2023 import VacancyFilter
from utils.additional_variables.additional_variables import table_list_for_checking_message_in_db as tables

db = DataBaseOperations(None)
filter = VacancyFilter()


def write_each_vacancy(results_dict):

    exist_or_not = db.check_vacancy_exists_in_db(
        tables_list=tables,
        title=results_dict['title'],
        body=results_dict['body']
    )

    if not exist_or_not:
        profession = filter.sort_profession(
            title=results_dict['title'],
            body=results_dict['body'],
            get_params=False,
            check_vacancy=True,
            check_vacancy_only_mex=True,
            check_contacts=False
        )
        profession = profession['profession']

        response_from_db = db.push_to_admin_table(
            results_dict=results_dict,
            profession=profession,
            check_or_exists=True
        )

        return {'response_from_db': response_from_db, "profession": profession}
    return {'response_from_db': exist_or_not, "profession": None}

async def get_name_session():
    current_session = DataBaseOperations(None).get_all_from_db(
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