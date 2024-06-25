from datetime import datetime, timedelta

from sites.write_each_vacancy_to_db import HelperSite_Parser
from db_operations.scraping_db import DataBaseOperations
from utils.additional_variables.additional_variables import admin_database
from filters.filter_jan_2023.filter_jan_2023 import VacancyFilter

hsite = HelperSite_Parser()
db = DataBaseOperations()
vacancy_filter = VacancyFilter()

async def redefine_prof_for_vacancies():
    vacancies = await get_vacancies_without_AI()
    statistics, vacancies_updated = await refresh_prof_by_AI(vacancies)
    print(f"\033[1;31mCRASHED AI: {statistics['crashed_AI']}\033[0m")
    print(f"\033[1;32mAI PROFESSION: {statistics['success_update']}\033[0m")


async def get_vacancies_without_AI(table_name=admin_database) -> list:
    fields = ['title', 'body', 'approved', 'profession', 'id']
    vacancies = db.get_all_from_db(table_name=table_name, param="WHERE approved='approves by filter'", field=', '.join(fields))
    return await compose_vacancies_to_dict(vacancies, fields)

async def get_vacancies_with_AI(table_name=admin_database, **kwargs) -> list:
    session_number = kwargs['session_number'] if kwargs.get('session_number') else None
    date_from = kwargs['date_from'] if kwargs.get('date_from') else (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
    date_to = kwargs['date_to'] if kwargs.get('date_to') else datetime.now().strftime("%Y-%m-%d")

    param = f"WHERE approved LIKE '%approved by ai%'" if table_name != 'archive' else f"WHERE profession='no_sort'"
    if session_number:
        param += f" AND session='{session_number}'"
    param += f" AND created_at between '{date_from}' AND '{date_to}'"
    fields = ['profession', 'title', 'body', 'approved', 'id']
    # fields = ['profession', 'approved', 'created_at']
    vacancies = db.get_all_from_db(table_name=table_name, param=param, field=', '.join(fields))
    return await compose_vacancies_to_dict(vacancies, fields)


async def compose_vacancies_to_dict(vacancies:list, fields:list) -> list:
    vacancies_dict = []
    for vacancy in vacancies:
        vacancy_dict = {}
        for i in range(0, len(fields)):
            vacancy_dict[fields[i]] = vacancy[i]
        vacancies_dict.append(vacancy_dict)
    return vacancies_dict

async def refresh_prof_by_AI(vacancies:list, to_db=True):
    vacancies_updated = {
        "crashed_AI": [],
        "success_update": []
    }
    update_vacancies_status = {
        "crashed_AI": 0,
        "success_update": 0,
    }
    for vacancy in vacancies:
        ai_profession, approved_status = await hsite.get_ai_profession(title=vacancy['title'], body=vacancy['body'])
        if approved_status and ai_profession:
            profession = hsite.filter.sort_profession(
                title=vacancy['title'],
                body=vacancy['body'],
                get_params=False,
                check_vacancy=True,
                check_vacancy_only_mex=True,
                check_contacts=False,
                vacancy_dict=vacancy,
                ai_profession=ai_profession if ai_profession else None
            )
            vacancy['profession'] = ", ".join(profession['profession']['profession'])
            print(f"\033[1;33mAI PROFESSION: {vacancy['profession']}\033[0m")
            vacancy['approved'] = approved_status
            print(f"\033[1;33mAPPROVED STATUS: {vacancy['approved']}\033[0m")
            if to_db:
                db.update_table_multi(table_name=admin_database, param=f"WHERE id={vacancy['id']}", values_dict=vacancy)
            vacancies_updated["success_update"].append(vacancy)
            update_vacancies_status['success_update'] += 1
        else:
            vacancies_updated["crashed_AI"].append(vacancy)
            update_vacancies_status['crashed_AI'] += 1
    return update_vacancies_status, vacancies_updated