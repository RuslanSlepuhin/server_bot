import time

# from db_operations.scraping_db import DataBaseOperations
# db = DataBaseOperations(None)

def compose_to_str_from_list(data_list):
    sub_str = ''
    for key in data_list:
        sub_str += f"{key}: {', '.join(data_list[key])}; "
    sub_str = sub_str[:-2]
    pass
    return sub_str


def decompose_from_str_to_list(data_str):
    data_dict = {}
    data_list = data_str.split('; ')
    for i in data_list:
        i = i.split(': ')
        key = i[0]
        sub_items = i[1]
        data_dict[key] = sub_items.split(', ')
    pass
    return data_dict

def compose_simple_list_to_str(data_list, separator):
    return f'{separator}'.join(data_list)

def string_to_list(text, separator):
    return text.split(separator)

def list_to_string(raw_list, separator):
    return separator.join(raw_list)

async def to_dict_from_admin_response(response, fields):
    response_dict = {}
    fields = fields.split(', ')
    for i in range(0, len(fields)):
        response_dict[fields[i]] = response[i]
    return response_dict

async def to_dict_from_temporary_response(response, fields):
    response_dict = {}
    fields = fields.split(', ')
    for i in range(0, len(fields)):
        response_dict[fields[i]] = response[i]
    return response_dict



