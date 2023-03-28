import pandas as pd
from db_operations.scraping_db import DataBaseOperations
from utils.additional_variables.additional_variables import parsing_report_path, table_parsing_report


class Reports:

    def __init__(self):
        self.db = DataBaseOperations()
        self.switch_to_next = False
        self.excel_row = {}
        self.excel_sheet = {}
        self.keys_fields = []
        self.fields_values_dict = {}
        self.keys = ['link_current_vacancy', 'title', 'body', 'check_link', 'found_id_by_link', 'found_title',
                     'found_body', 'found_id', 'found_vacancy_link', 'has_been_added_to_db', 'error', 'not_contacts',
                     'not_vacancy', 'profession', 'ma', 'mex']
        # self.db.delete_table(table_name=table_parsing_report)

    def parsing_report(self, **kwargs):
        if kwargs:
            for key in kwargs:
                if key in self.keys:
                    self.excel_row[key] = kwargs[key]

    def parsing_switch_next(self, switch=None):
        if switch:
            for i in self.keys:
                if i not in self.excel_row:
                    if i in ['has_been_added_to_db', 'not_contacts', 'not_vacancy']:
                        self.excel_row[i] = False
                    else:
                        self.excel_row[i] = '-'
            for key in self.excel_row:
                if key not in self.excel_sheet:
                    self.excel_sheet[key] = []
                self.excel_sheet[key].append(self.excel_row[key])
            self.print_data()

            # for key in self.keys:
            #     if key in ['has_been_added_to_db', 'not_contacts', 'not_vacancy']:
            #         self.keys_fields.append(f"{key} BOOLEAN")
            #     elif key in ['title', 'body']:
            #         self.keys_fields.append(f"{key} VARCHAR(10000)")
            #     else:
            #         self.keys_fields.append(f"{key} VARCHAR(150)")
            #
            # self.db.create_table_common(
            #     field_list=self.keys_fields,
            #     table_name='report_parsing_temporary'
            # )
            #
            # self.db.push_to_db_common(
            #     table_name='report_parsing_temporary',
            #     fields_values_dict=self.excel_row
            # )

            self.excel_row = {}

    def print_data(self):
        print('*'*10)
        for key in self.excel_row:
            value = self.excel_row[key][:30].replace('\n', ' ') \
                if type(self.excel_row[key]) is str \
                else self.excel_row[key]
            print(f"{key}: {value}")
        print('*'*10)
        pass

    async def add_to_excel(self):
        self.excel_row = {}
        df = pd.DataFrame(self.excel_sheet)
        try:
            df.to_excel(parsing_report_path, sheet_name='Sheet1')
            print('got it')
            return True
        except Exception as e:
            print(f"Something is wrong: {str(e)}")
            return False
