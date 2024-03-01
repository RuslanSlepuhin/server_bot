from utils.additional_variables import additional_variables as variables
import pandas as pd

class VacanciesTitleReport:
    """
    This classes methods return excel report to customer with vacancies titles from database
    to compare with vacancies sources
    """
    def __init__(self, main_class, message):
        self.main_class = main_class
        self.message = message
        self.path = "./report/excel/"
        self.report_name = "vacancies_title.xlsx"

    def get_titles_from_db(self, fields, conditions) -> str:
        data = self.get_from_db(fields, conditions)
        return self.write_data_to_excel(data, fields) if data else ""

    def get_from_db(self, fields, conditions) -> dict:
        responses = self.main_class.db.get_all_from_db(table_name=variables.vacancies_database, field=", ".join(fields), param=f"WHERE {conditions}")
        if responses:
            data = {}
            for i in fields:
                data[i] = []
            for response in responses:
                for i in range(0, len(fields)):
                    data[fields[i]].append(response[i])
            return data
        else:
            self.main_class.bot.send_message(self.message.chat.id, "No data in database")
            return {}

    def write_data_to_excel(self, data, fields) -> str:
        df = pd.DataFrame(data)
        path = self.path + self.report_name
        df.to_excel(path, sheet_name='Sheet1')
        print('PD EXCEL DONE')
        return path
