"""{
 "direction": "",
 "specialization": [],
 "programmingLanguage": [], - это на данном этапе в верстке не реализовано, будет приходить пустой массив
 "technologies": [], - это на данном этапе в верстке не реализовано, будет приходить пустой массив
 "level": ["", "trainee", "entry level", "junior", "middle", "senior", "director", "lead"],
 "country": [],
 "city": [],
 "state": [], - это на данном этапе в верстке не реализовано, будет приходить пустой массив
 "salary": ["", ""],
        "currency": "",
 "salaryOption": ["Почасовая", "За месяц", "За год", "До вычета налогов", "На руки"],
 "companyScope": [],
 "typeOfEmployment": ["", "fulltime", "parttime", "contract", "freelance", "internship", "volunteering"],
 "companyType": ["", "product", "outsourcing", "outstaff", "consulting", "notTechnical", "startup"],
 "companySize": ["1-200", "201-500", "501-1000", "1000"],
 "job_type": ["remote", "fulltime", "flexible", "office", "office/remote" ]
 }"""

"""
The JSON above means how many fields you will receive, them types and values. It's will be static values from check boxes 
exception direction.
The direction field will contain free text.

How I'm doing it:
1. The direction field I can search:
  - through a pattern. I can find all keys words and choose vacancies by this professions. But it will take a more time 
    for pattern loop and get by request from database next step
 - in fields: title, body, profession
 
 I like the second method
 
2. Specialization - there are too many different values to search them in the profession, vacancy, body, title by "OR"

3. Level - the search in level fields. It's more easy than other tasks

4. Country - search in country field in backend. No that field now. I will create it and do the function for searching 
    country.

5. City - the same

6. Salary has two values from and till summ, Currency contain Eur, USD, BYR, RuR for example. I need to get from back 
    vacancies between this values 
 
7. salaryOption - I need to make the method for find this values from text. Add to database the same field with the same 
    values

8. typeOfEmployment - to create the same field in tables and to fill the same values. To find it in the body, the title    

9. companyType - static values. I need to create the same fields in tables on backend and fill them. 

10. companySize - the same

11. job_type - this field exists, but contains only one value - remote. Need to create method for search and fill 
    others static values.  
"""

class Predictive():
    def __init__(self):
        pass

    def direction_method(self, text, fields_list):
        part_of_request = '('
        if not text:
            return ''
        for field in fields_list:
            part_of_request += f"LOWER({field}) LIKE '%{text.lower()}%' OR "
        return part_of_request[:-4] + ')'

    def get_part_of_query(self, request_list, fields_list, dict_name):
        words_list = []
        part_of_request = '('
        if not request_list:
            return ''
        if type(request_list) is str:
            request_list = [request_list,]

        # compose the list from helper dict values by each key
        for key_word in request_list:
            if key_word:
                if key_word in dict_name:
                    words_list.extend(dict_name[key_word.lower()])
                else:
                    words_list.append(key_word.lower())

        for word in words_list:
            part_of_request += f"{self.direction_method(word, fields_list)} OR "

        part_of_request = part_of_request[:-4]
        if part_of_request:
            return part_of_request + ")"
        else:
            return ''

    def get_query_salary(self, request_from_frontend, fields_list):
        return ""

    def get_full_query(self, request_from_frontend):
        query = ''
        part_of_query = ''
        for key in request_from_frontend:

            if key == 'level':
                fields_list = ['level']
            elif key == 'job_type':
                fields_list = ['job_type']
            elif key == 'salary':
                fields_list = ['salary']
                part_of_query = self.get_query_salary(request_from_frontend[key], fields_list)
            else:
                fields_list = ['body', 'title', 'vacancy', 'profession']

            if key not in ['salary',]:
                part_of_query = Predictive().get_part_of_query(
                    request_list=request_from_frontend[key],
                    fields_list=fields_list,
                    dict_name=key
                )
            if part_of_query:
                query += f"({part_of_query}) AND "
        if query:
            # query = f"SELECT * FROM admin_last_session WHERE {query[:-5]}"
            query = f"WHERE {query[:-5]}"
        return query

# result = Predictive().get_full_query(request_from_frontend=request_from_frontend)
# print(result)
