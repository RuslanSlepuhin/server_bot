import re
from helper_functions.parser_find_add_parameters import parser_find_data

class FinderAddParameters:

    def __init__(self,):
        pass

    def clean_text_special_symbols(self, main_dict=True, input_dict=None):
        special_symbols = {}
        if main_dict:
            special_symbols = parser_find_data.special_symbols
        if type(input_dict) is dict:
            special_symbols.update(input_dict)
        for item in special_symbols:
            self.text = self.text.replace(item, special_symbols[item])

    def salary_to_set_form(self, **kwargs):
        currency_dict = parser_find_data.currency_dict

        self.text = kwargs['text'] if 'text' in kwargs else ''
        if not self.text:
            response = ['-', '-', '-', '-']
            print(response)
            return response

        self.region = kwargs['region'] if 'region' in kwargs else None
        match self.region:
            case "BY": currency_dict =  parser_find_data.by_dict

        # search numbers
        print('-'*10)
        print('add_parameters: self.text: ', self.text)
        self.clean_text_special_symbols()
        match = re.findall(r"[0-9,]+[\s]?[0-9]+[\s]?[0-9]{0,4}", self.text)
        self.salary_list = [number.replace(' ', '').replace(',', '') for number in match]
        if 'тыс' in self.text:
            salary_list = []
            for number in self.salary_list:
                salary_list.append(f"{number}000")
            self.salary_list = salary_list


        # search currency
        if self.salary_list:
            match = []
            if len(self.salary_list) < 2:
                self.salary_list.append('-')
            for key in currency_dict:
                match = re.findall(fr"{key.lower()}", self.text.lower())
                if match and match[0]:
                    self.salary_list.append(currency_dict[key])
                    break
            if not match:
                salary = self.salary_list[0]
                if len(salary) > 5:
                    self.salary_list.append('RuR')
            if len(self.salary_list)<3:
                self.salary_list.append('-')

        # searching Per Period
        if self.salary_list:
            match = []
            period_dict = parser_find_data.period_dict
            for period in period_dict:
                for value in period_dict[period]:
                    match = re.findall(fr"{value.lower()}", self.text.lower())
                    if match and match[0]:
                        self.salary_list.append(period)
                        break
            if not match and len(self.salary_list) < 4:
                self.salary_list.append('Per Month')

        if not self.salary_list:
            self.salary_list = ['-', '-', '-', '-']

        print(self.salary_list)

        return self.salary_list

# f= FinderAddParameters()
# f.salary_to_set_form(text='$15,000 - $30,000 ')