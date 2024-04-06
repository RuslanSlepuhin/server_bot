import json
import re

import pandas as pd
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from _apps.web_form_bot import variables
import requests
from _apps.simpleatom.form.variables.variables import common_field_name

class HelperBot:

    def __init__(self, **kwargs):
        self.bot_class = kwargs['bot_class'] if kwargs.get('bot_class') else None

    async def replyMarkupBuilder(self, *args, **kwargs):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        for button in args:
            keyboard.add(KeyboardButton(button))
        return keyboard

    async def send_form_excel(self) -> [str, bool]:
        excel_dict = {}
        responses = requests.get(url=f"{variables.server_domain}{variables.endpoint_form}")
        if 200 <= responses.status_code < 400 and responses:
            responses = responses.json()
            # responses = json.loads(responses.content.decode('utf-8'))['response']
            for item in responses:
                # if not item.get('name'):
                #     item['name'] = "-"
                union_fields = await self.union_fields_from_responses(responses)
                add_keys = await self.union_add_fields_from_responses(responses) - union_fields
                for key in union_fields:
                    if key != common_field_name:
                        excel_dict = await self.get_value_from_element(key, item, excel_dict)
                        # if key not in excel_dict:
                        #     excel_dict[key] = []
                        # excel_dict[key].append(item[key]) if item.get(key) else "-"
                    else:
                        for add_key in add_keys:
                            excel_dict = await self.get_value_from_element(add_key, item[key], excel_dict)
                            # if add_key not in excel_dict:
                            #     excel_dict[add_key] = []
                            # excel_dict[add_key].append(item[key][add_key]) if item[key].get(add_key) else "-"


            df = pd.DataFrame(excel_dict)

            file_full_path = variables.media_excel_path + variables.form_excel_name
            df.to_excel(file_full_path, sheet_name='Sheet1')
            print(f'\nExcel was writting')
            return file_full_path
        else:
            return False

    async def get_value_from_element(self, key, element, excel_dict) -> list:
        if key not in excel_dict:
            excel_dict[key] = []
        excel_dict[key].append(element[key]) if element.get(key) else excel_dict[key].append("-")
        return excel_dict

    async def send_file(self, bot, message, file_full_path, caption=variables.caption_send_file) -> bool:
        with open(file_full_path, 'rb') as file:
            try:
                await bot.send_document(message.chat.id, file, caption=caption)
            except Exception as ex:
                await bot.send_message(message.chat.id, ex)
                return False

    async def text_object_from_form(self, data:dict) -> str:
        text = ""
        if "formName" in data:
            text += f"Form: {data['formName']}\n\n"
            data.pop('formName')
        # if "submit" in data:
        #     text += f"Form: {data['submit']}\n\n"
        #     data.pop('submit')
        backslash = "\\"
        for key in data:
            if type(data[key]) not in [tuple, list]:
                text += f"{key}\n- {data[key]}\n\n"
            else:
                data_key_str = "\n- " if data[key] else ""
                data_key_str += "\n- ".join(data[key])
                text += f"{key}{data_key_str}\n\n"
            # text += f"{key}\n- {data[key]}\n\n" if type(data[key]) not in [tuple, list] else f"{key} {backslash}n- '.join(data[key])\n\n"
        return text

    async def matching(self, text, pattern):
        match = re.findall(pattern, text)
        return True if match else False


    async def union_fields_from_responses(self, responses:list) -> set:
        keys_set = set()
        for response in responses:
            keys = response.keys()
            keys_set = keys_set.union(set(keys))
        return keys_set

    async def union_add_fields_from_responses(self, responses) -> set:
        keys_set = set()
        for response in responses:
            if response.get(common_field_name):
                keys = response[common_field_name].keys()
                keys_set = keys_set.union(set(keys))
        return keys_set