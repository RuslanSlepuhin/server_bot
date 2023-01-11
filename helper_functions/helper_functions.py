import time
from patterns._export_pattern import export_pattern

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
        if sub_items:
            data_dict[key] = sub_items.split(', ')
        else:
            data_dict[key] = []
    # for key in data_dict:
    #     if data_dict[key] == ['']:
    #         data_dict[key] = []
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

async def get_pattern(path):
    print('\n\n---------------------------------------\n\n')
    message = ''
    for key in export_pattern:
        message += f"{key}:\n"

        if type(export_pattern[key]) is dict:
            for key2 in export_pattern[key]:
                message += f"\t{key2}:\n"

                if type(export_pattern[key][key2]) is dict:
                    for key3 in export_pattern[key][key2]:
                        message += f"\t\t{key3}:\n"

                        if type(export_pattern[key][key2][key3]) is dict and export_pattern[key][key2][key3]:
                            for key4 in export_pattern[key][key2][key3]:
                                message += f"\t\t\t{key4}:\n"

                                if type(export_pattern[key][key2][key3][key4]) is dict:
                                    for key5 in export_pattern[key][key2][key3][key4]:
                                        message += f"\t\t\t\t{key5}:\n"

                                        if type(export_pattern[key][key2][key3][key4][key5]) is dict:
                                            for key6 in export_pattern[key][key2][key3][key4][key5]:
                                                message += f"\t\t\t\t\t{key6}:\n"
                                        else:
                                            message += f"\t\t\t\t\t\t{export_pattern[key][key2][key3][key4][key5]}\n"
                                else:
                                    message += f"\t\t\t\t\t{export_pattern[key][key2][key3][key4]}\n"
                        else:
                            message += f"\t\t\t{export_pattern[key][key2][key3]}\n"
                else:
                    message += f"\t\t{export_pattern[key][key2]}\n"
        else:
            message += f"\t{export_pattern[key]}\n"

    print(message)
    with open(path, "w", encoding='utf-8') as file:
        file.write(message)
        print('Done')



