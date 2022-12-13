from db_operations.scraping_db import DataBaseOperations
from filters.scraping_get_profession_Alex_next_2809 import AlexSort2809
db = DataBaseOperations(None)
filter = AlexSort2809()

def write_each_vacancy(results_dict):

    # profession = filter.sort_by_profession_by_Alex(
    #     title=results_dict['title'],
    #     body=results_dict['body'],
    #     # companies=None,
    #     get_params=False,
    #     only_profession=True
    # )
    profession = filter.sort_by_profession_by_Alex(
        title=results_dict['title'],
        body=results_dict['body'],
        # companies=None,
        get_params=False,
        check_vacancy=False,
        check_contacts=False
    )
    profession = profession['profession']

    response_from_db = db.push_to_admin_table(results_dict, profession)
    return {'response_from_db': response_from_db, "profession": profession}

# def file():
#     results_dict = {}
#     text = ''
#     body = ''
#     with open('./../text.txt', 'r') as file:
#         text = file.read()
#
#     title = text.split('/n', 1)[0]
#     results_dict['title'] = title
#     results_dict['body'] = body
#     write_each_vacancy(results_dict)
#
# file()
