import json
import pandas as pd
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from telegram import variables
import requests
from aiogram.types import FSInputFile

class HelperBot:

    def __init__(self, **kwargs):
        self.bot_class = kwargs['bot_class'] if kwargs.get('bot_class') else None

    async def replyMarkupBuilder(self, *args, **kwargs):
        builder = ReplyKeyboardBuilder()
        for button in args:
            builder.button(text=button)
        return builder.as_markup(resize_keyboard=True)

    async def send_form_excel(self) -> str:
        excel_dict = {}
        responses = requests.get(url=f"{variables.server_domain}{variables.endpoint_form}")
        responses = json.loads(responses.content.decode('utf-8'))['response']
        for item in responses:
            if not item.get('name'):
                item['name'] = "-"
            for key in item:
                if key not in excel_dict:
                    excel_dict[key] = []
                excel_dict[key].append(item[key])

        df = pd.DataFrame(
            {
                'id': excel_dict['id'],
                'name': excel_dict['name'],
                'instrumentWorks': excel_dict['instrumentWorks'],
                'whatAmount': excel_dict['whatAmount'],
                'whatTradingStrategy': excel_dict['whatTradingStrategy'],
                'optimalInvestmentPeriod': excel_dict['optimalInvestmentPeriod'],
                'howToReach': excel_dict['howToReach'],
            }
        )

        file_full_path = variables.media_excel_path + variables.form_excel_name
        df.to_excel(file_full_path, sheet_name='Sheet1')
        print(f'\nExcel was writting')
        return file_full_path

    async def send_file(self, message, file_full_path, caption=variables.caption_send_file) -> bool:
        try:
            file = FSInputFile(file_full_path)
            await self.bot_class.bot.send_document(chat_id=message.chat.id, document=file, caption=caption)
            return True
        except Exception as ex:
            await self.bot_class.bot.send_message(message.chat.id, ex)
            return False

    async def text_object_from_form(self, data:dict) -> str:
        text = ""
        for key in data:
            text += f"{variables.keys_as_questions[key]}\n- {data[key]}\n\n" if key in variables.keys_as_questions else f"{key}: {data[key]}\n\n"
        return text



