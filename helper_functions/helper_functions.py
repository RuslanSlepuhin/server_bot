

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
