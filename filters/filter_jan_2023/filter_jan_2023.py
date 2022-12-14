import re
from patterns import pattern_Alex2809
from db_operations.scraping_db import DataBaseOperations
# from patterns.pattern_Alex2809 import search_companies, search_companies2, english_pattern, remote_pattern, \
#     relocate_pattern, middle_pattern, senior_pattern, vacancy_name, vacancy_pattern, contacts_pattern, profession_new_pattern
from patterns._export_pattern import export_pattern as q
from utils.additional_variables import additional_variables as variables

class VacancyFilter:

    def __init__(self):
        self.pattern_alex = pattern_Alex2809.pattern
        self.capitalize = ['pm', 'game', 'designer', 'hr', 'analyst', 'qa', 'ba', 'product']

        self.result_dict2 = {'vacancy': 0, 'contacts': 0, 'fullstack': 0, 'frontend': 0, 'backend': 0, 'pm': 0,
                             'mobile': 0, 'game': 0, 'designer': 0, 'hr': 0, 'analyst': 0, 'qa': 0, 'ba': 0,
                             'product': 0, 'devops': 0, 'marketing': 0, 'sales_manager': 0, 'junior': 0, 'middle': 0,
                             'senior': 0}

        self.keys_result_dict = ['fullstack', 'frontend', 'qa', 'ba', 'backend', 'pm', 'mobile', 'game', 'designer',
                                 'hr', 'analyst', 'product', 'devops', 'marketing', 'sales_manager']
        self.valid_profession_list = ['marketing', 'ba', 'game', 'product', 'mobile',
                                      'pm', 'sales_manager', 'analyst', 'frontend',
                                      'designer', 'devops', 'hr', 'backend', 'frontend', 'qa', 'junior']
        self.export_pattern = q
        self.not_lower_professions = variables.not_lower_professions
        self.excel_dict = {}

    def sort_profession(self, title, body, check_contacts=True, check_profession=True, check_vacancy=True, get_params=True):
        profession = dict()
        profession['tag'] = ''
        profession['anti_tag'] = ''
        profession['profession'] = []
        profession['sub'] = []
        params = {}
        vacancy = f"{title}\n{body}"
        patt = q

        if check_profession:
            # if it is not vacancy, return no_sort
            if check_vacancy:
                result = self.check_parameter(
                    pattern=self.export_pattern['data']['vacancy'],
                    vacancy=vacancy,
                    key='vacancy'
                )
                self.result_dict2['vacancy'] = result['result']
                profession['tag'] += result['tags']
                profession['anti_tag'] += result['anti_tags']

                if not self.result_dict2['vacancy']:
                    profession['profession'] = {'no_sort'}
                    print(f"line84 {profession['profession']}")
                    print("= vacancy not found =")
                    return {'profession': profession, 'params': {}}

            if check_contacts:
                # if it is without contact, return no_sort
                result = self.check_parameter(
                    pattern=self.export_pattern['data']['contacts'],
                    vacancy=vacancy,
                    key='contacts'
                )
                self.result_dict2['contacts'] = result['result']
                profession['tag'] += result['tags']
                profession['anti_tag'] += result['anti_tags']

                if not self.result_dict2['contacts']:
                    profession['profession'] = {'no_sort'}
                    print(f"not contacts {profession['profession']}")
                    print("= contacts not found =")
                    return {'profession': profession, 'params': {}}

            # ---------------- professions -----------------

            for item in self.valid_profession_list:
                if item in self.not_lower_professions:
                    low = False
                else:
                    low = True

                if item == 'product':
                    item = 'pm'

                result = self.check_parameter(
                    pattern=self.export_pattern['professions'][item],
                    vacancy=vacancy,
                    low=low,
                    key=item
                )
                if result['result']:
                    profession['profession'].append(result['result'])
                    # print(f"in loop: {profession['profession']}")
                profession['tag'] += result['tags']
                profession['anti_tag'] += result['anti_tags']

            if 'fullstack' in profession['profession']:
                profession = self.transform_fullstack_to_back_and_front(text=vacancy, profession=profession)

            if not profession['profession']:
                profession['profession'] = {'no_sort'}
                # print(f"line100 {profession['profession']}")

            profession['profession'] = set(profession['profession'])

            # -------------- get subprofessions -------------------------
            if 'no_sort' not in profession['profession']:
                print(f"FINALLY: {profession['profession']}")
                self.get_sub_profession(profession, text=vacancy)
            else:
                profession['sub'] = []

            if profession['sub']:
                profession = self.compose_junior_sub(
                    profession=profession,
                    key_word='junior'
                )
        # --------------------- end -------------------------
        if get_params:
            params = self.get_params(text=vacancy, profession=profession)



        return {'profession': profession, 'params': params}

    def get_sub_profession(self, profession, text):
        profession['sub'] = {}

        # print(text)
        # print(profession['profession'])
        for prof in profession['profession']:
            prof = prof.strip()

            union_sub = {}
            if prof in self.valid_profession_list:
                profession['sub'][prof] = []
                current_profession_sub_list = self.export_pattern['professions'][prof]['sub']
                for sub in current_profession_sub_list:
                    pattern = self.export_pattern['professions'][prof]['sub'][sub]

                    result = self.check_parameter(
                        pattern=pattern,
                        vacancy=text,
                        key=sub,
                        low=False
                    )
                    if result['result']:
                        profession['sub'][prof].append(result['result'])

        for i in profession['sub']:
            print(i, profession['sub'][i])
        pass
        return profession

    def check_parameter(self, pattern, vacancy, key, low=True):
        result = 0
        tags = ''
        anti_tags = ''

        # if low:
        #     vacancy = vacancy.lower()
        for word in pattern['ma']:
            # if low:
            #     word = word.lower()
            match = set(re.findall(rf"{word}", vacancy))

            if match:
                result += len(match)
                tags += f'MA {key}={match}\n'

        if result:
            for anti_word in pattern['mex']:
                # if low:
                #     anti_word = anti_word.lower()

                match = set(re.findall(rf"{anti_word}", vacancy))
                if match:
                    result = 0
                    anti_tags += f'MEX {key}={match}\n'
                    break
        else:
            anti_tags = ''
        return {'result': key if result else '', 'tags': tags, 'anti_tags': anti_tags}

    def get_params(self, text, profession, all_fields_null=False):
        params = {}
        params['company'] = self.get_company_new(text)
        params['job_type'] = self.get_remote_new(text)
        params['relocation'] = self.get_relocation_new(text)
        params['english'] = self.english_requirements_new(text)
        params['vacancy'] = self.get_vacancy_name(text, profession['profession'])
        return params

    def transform_fullstack_to_back_and_front(self, text, profession):

        for anti_word in self.pattern_alex['backend']['mex']:
            match = re.findall(rf"{anti_word.lower()}", text.lower())
            if match:
                profession['anti_tag'] += f'TAG ANTI backend={match}\n'
            else:
                profession['profession'].add('backend')

        for anti_word in self.pattern_alex['frontend']['mex']:
            match = re.findall(rf"{anti_word.lower()}", text.lower())
            if match:
                profession['anti_tag'] += f'TAG ANTI frontend={match}\n'
            else:
                profession['profession'].add('frontend')

        profession['profession'].discard('fullstack')

        return profession

    def get_company_new(self, text):
        companies_from_db = DataBaseOperations(None).get_all_from_db(
            table_name='companies',
            without_sort=True,
            field='company'
        )
        for company in companies_from_db:
            company = company[0]
            if company and company in text:
                # print(company)
                return company

        match = re.findall(rf"{self.export_pattern['others']['company']['ma']}", text)
        if match:
            return self.clean_company_new(match[0])

        match = re.findall(rf"{self.export_pattern['others']['company2']['ma']}", text)
        if match:
            return match[0]
        return ''

    def english_requirements_new(self, text):
        english_pattern = "|".join(self.export_pattern['others']['english']['ma'])
        match = re.findall(english_pattern, text)
        if match:
            match = match[0].replace('\n', '').replace('"', '').replace('#', '').replace('.', '')
            match = match.strip()
            if match[-1:] == '(':
                match = match[:-1]
        else:
            match = ''
        return match

    def get_relocation_new(self, text):
        relocate_pattern = "|".join(self.export_pattern['others']['relocate']['ma'])
        match = re.findall(rf"{relocate_pattern}", text)
        if match:
            return match[0]
        else:
            return ''

    def get_remote_new(self, text):
        remote_pattern = "|".join(self.export_pattern['others']['remote']['ma'])
        match = re.findall(rf"{remote_pattern}", text)
        if match:
            return match[0]
        else:
            return ''

    def clean_company_new(self, company):
        pattern = "^[Cc]ompany[:]{0,1}|^[????]??????????????[:]{0,1}" #clear company word
        pattern_russian = "[??-????-??\s]{3,}"
        pattern_english = "[a-zA-Z\s]{3,}"

        # -------------- if russian and english, that delete russian and rest english -----------
        if re.findall(pattern_russian, company) and re.findall(pattern_english, company):
            match = re.findall(pattern_english, company)
            company = match[0]

        # -------------- if "company" in english text, replace this word
        match = re.findall(pattern, company)
        if match:
            company = company.replace(match[0], '')

        return company.strip()

    def get_vacancy_name(self, text, profession_list):
        vacancy = ''
        vacancy_pattern = self.export_pattern['others']['vacancy']['sub']['common_vacancy']
        match = re.findall(rf"{vacancy_pattern}", text)
        if match:
            vacancy = match[0]
        else:
            for pro in profession_list:
                if pro == 'no_sort':
                    pattern = self.export_pattern['others']['vacancy']['sub']['backend_vacancy']
                else:
                    pattern = pattern = self.export_pattern['others']['vacancy']['sub'][f'{pro}_vacancy']
                match = re.findall(rf"{pattern}", text)
                if match:
                    vacancy = match[0]
                    break

            if not vacancy:
                pattern = self.export_pattern['others']['vacancy']['sub']['backend_vacancy']
                match = re.findall(rf"{pattern}", text)
                if match:
                    vacancy = match[0]
        if vacancy:
            vacancy = re.sub(r"[????]????????????????[:\s]{1,2}", '', vacancy)
            vacancy = re.sub(r"[????]??????????????[:\s]{1,2}", '', vacancy)
            vacancy = vacancy.strip()

            vacancy = self.clean_vacancy_from_get_vacancy_name(vacancy)
        return vacancy

    def clean_vacancy_from_get_vacancy_name(self, vacancy):
        trash_list = ["[????]?????? ?? ??????????????[:]?", "[????]????????????????[:]?", "[????]??????[:]?", "[????]??????????????[:]?", "[????]????????????[:]?",
                      "[????]????????????????[:]?", "?? ????????????[:]?", "[????]?????????????? ????????????????[:]?", "[VACANCYvacancy]{7}[:]?"]
        for i in trash_list:
            vacancy = re.sub(rf"{i}", "", vacancy)

        return vacancy.strip()

    def compose_junior_sub(self, profession, key_word):
        print("profession['sub'] ", profession['sub'])
        if key_word in profession['sub'].keys():
            for key in profession['sub'].keys():
                if key != key_word:
                    profession['sub'][key_word].append(key)
        return profession

