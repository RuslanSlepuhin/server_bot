import configparser

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

from _apps.coffee_customer_bot_apps.variables import variables

config = configparser.ConfigParser()
config.read("./coffee_customer_bot_apps/settings/config.ini")

class HorecaBot:
    # print('HorecaBot has been started\nhttps://t.me/medicine_card_bot\n')

    def __init__(self, token=None):
        self.token = token if token else config['Bot']['horeca_token']
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.test_data = {'user_id': 648154559, 'id_horeca': 3, 'id_order': '7fa99e', 'status': 'canceled_by_user'}

    def bot_handlers(self):

        @self.dp.message_handler(commands=['get_users'])
        async def get_users(message: types.Message):
            pass

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await self.bot.send_message(message.chat.id, "Hey")
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = KeyboardButton("Заказ готов")
            button2 = KeyboardButton("Заказ протух")
            keyboard.add(button1, button2)
            await self.bot.send_message(message.chat.id, "PRESS BUTTON", reply_markup=keyboard)
            pass

        @self.dp.callback_query_handler()
        async def callbacks(callback: types.CallbackQuery):
            pass

        @self.dp.message_handler(content_types=['text'])
        async def text_message(message):
            self.test_data['user_id'] = message.chat.id
            self.test_data['status'] = message.text

            if message.text == 'Заказ готов':
                print('send from bot')
                requests.post(f"{variables.server_domain}{variables.server_test_status_endpoint_from_horeca}",
                              json=self.test_data)
                print('sent from bot')
            elif message.text == "Заказ протух":
                requests.post(f"{variables.server_domain}{variables.server_test_status_endpoint_from_horeca}",
                              json=self.test_data)

        executor.start_polling(self.dp, skip_updates=True)

    async def custom_send_message(self, data):
        user_id = data['user_id']
        await self.bot.send_message(user_id, str(data))