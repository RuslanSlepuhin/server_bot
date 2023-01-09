from db_operations.scraping_db import DataBaseOperations
from filters.filter_jan_2023.filter_jan_2023 import VacancyFilter

db = DataBaseOperations(None)
filter = VacancyFilter()


def write_each_vacancy(results_dict):

    profession = filter.sort_profession(
        title=results_dict['title'],
        body=results_dict['body'],
        get_params=False,
        check_vacancy=False,
        check_contacts=False
    )
    profession = profession['profession']

    response_from_db = db.push_to_admin_table(
        results_dict=results_dict,
        profession=profession,
        check_or_exists=True
    )
    return {'response_from_db': response_from_db, "profession": profession}

