import configparser
import json

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from _apps.coffee_customer_bot_apps.variables import variables
from _apps.coffee_customer_bot_apps.coffee_customer_bot.coffee_customer_bot_addit_methods import CustBotAddMethods
from _apps.coffee_customer_bot_apps.coffee_customer_bot.coffee_customer_bot_addit_methods import FormVerificationCode
# from coffee_customer_bot_apps.database.database_methods import DataBase

config = configparser.ConfigParser()
config.read("./_apps/coffee_customer_bot_apps/settings/config.ini")

class CustomerBot:
    def __init__(self, token=None):
        self.token = token if token else config['Bot']['customer_token']
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.bot_methods = CustBotAddMethods(bot=self.bot)
        self.user_data = variables.user_data
        # self.database_methods = DataBase()
        self.messages_list = []
        self.status_number = 0

    def bot_handlers(self):

        @self.dp.message_handler(state=FormVerificationCode.code)
        async def process_api_id(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['code'] = message.text
                self.user_data['enter_key'] = message.text
            await state.finish()
            url = variables.server_domain + variables.verification_endpoint

            response = requests.post(url, json=self.user_data)
            print(response.status_code)
            # await self.bot_methods.start_dialog_with_user(message)

            jsonResponse = json.loads(response.content.decode('utf-8'))
            # -------------------- !!! check the response from the server ---------------------
            if jsonResponse['message'] in ["Данные успешно обновлены", "Пользователь уже зарегистрирован"]:
                await self.bot_methods.start_dialog_with_user(message)
            elif jsonResponse['message'] == "Неверный enter_key":
                self.messages_list.append(await self.bot.send_message(message.chat.id, variables.dialog_customer['verification_error']))
                await self.bot_methods.verify_user(message)


        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await self.bot.send_message(message.chat.id, f"user id {message.chat.id}")
            await self.start(message)


        # @self.dp.callback_query_handler()
        # async def callbacks(callback: types.CallbackQuery):
        #     pass
        #
        # @self.dp.message_handler(commands=['commands'])
        # async def get_users(message: types.Message):
        #     pass
        #
        @self.dp.message_handler(content_types=['text'])
        async def text_message(message):
            self.user_data['telegram_user_id'] = message.chat.id
            self.user_data['status'] = message.text

            if message.text in variables.customer_buttons_status:
                self.user_data['status'] = variables.customer_buttons_status[message.text]
                requests.post(f"{variables.server_domain}{variables.server_test_status_endpoint_from_customer}",
                              json=self.user_data)

            else:
                await self.bot.delete_message(message.chat.id, message.message_id)

        executor.start_polling(self.dp, skip_updates=True)

    async def custom_send_message(self, data):
        self.user_data = data
        user_id = data['telegram_user_id']
        status_text = str(data)
        # status_text = f"{variables.status_text_customer}{data['id_order']}: {data['status']}"
        await self.bot.send_message(user_id, status_text)

    async def check_subscriber(self, user_id):
        try:
            msg = await self.bot.send_message(int(user_id), "Вы можете отслеживать Ваш заказ в этом боте")
            self.user_data['bot_subscribing'] = True
            await msg.delete()
            return True
        except:
            self.user_data['bot_subscribing'] = False
            return False

    async def start(self, message):
        # url = variables.server_domain + variables.get_user_verification_info
        # response = requests.get(url)
        # json_response = json.loads(response.content.decode('utf-8'))
        #
        # if await self.bot_methods.check_start(json_response):
        #     return await self.bot_methods.start_dialog_with_user(message)

        self.user_data['telegram_user_id'] = message.chat.id
        self.user_data['bot_subscribing'] = True
        self.user_data['enter_key'] = self.user_data[
            'enter_key'] if 'enter_key' in self.user_data else ""

        if self.user_data['telegram_user_id'] and self.user_data['enter_key']:
            await self.bot_methods.start_dialog_with_user(message)
        elif not self.user_data['enter_key']:
            await self.bot_methods.verify_user(message)
        else:
            self.messages_list.append(await self.bot.send_message(message.chat.id,
                                                                  "Something is damage in START method. Looking for errors there"))

