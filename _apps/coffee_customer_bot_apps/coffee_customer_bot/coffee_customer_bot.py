import asyncio
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

config = configparser.ConfigParser()
config.read("./_apps/coffee_customer_bot_apps/settings/config.ini")

class CustomerBot:
    def __init__(self, token=None):
        self.token = token if token else config['Bot']['customer_token']
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.bot_methods = CustBotAddMethods(self.bot, self)
        self.user_data = variables.user_data
        # self.database_methods = DataBase()
        self.messages_list = []
        self.status_number = 0
        self.order_index = 0
        self.user_orders = []
        self.msg = None

    def bot_handlers(self):

        @self.dp.message_handler(state=FormVerificationCode.code)
        async def process_api_id(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['code'] = message.text
                self.user_data['enter_key'] = message.text
            await state.finish()
            url = variables.server_domain + variables.send_enterkey_endpoint
            response = requests.post(url, json=self.user_data)
            print(response.status_code)
            # await self.bot_methods.start_dialog_with_user(message)

            jsonResponse = json.loads(response.content.decode('utf-8'))
            # -------------------- !!! check the response from the server ---------------------
            if jsonResponse['message'] in ["Данные успешно обновлены", "Пользователь уже зарегистрирован"]:
                await self.bot_methods.dialog_with_user(message)
            elif jsonResponse['message'] == "Неверный enter_key":
                self.messages_list.append(await self.bot.send_message(message.chat.id, variables.dialog_customer['verification_error']))
                await self.bot_methods.verify_user()

        @self.dp.callback_query_handler()
        async def catch_callback(callback: types.CallbackQuery):
            if callback.data == ">>":
                await self.bot_methods.refresh_user_orders(callback.message)
                self.order_index += 1
                await self.bot_methods.dialog_with_user()

            if callback.data == "<<":
                await self.bot_methods.refresh_user_orders(callback.message)
                self.order_index -= 1
                await self.bot_methods.dialog_with_user()

            if callback.data in variables.USER_STATUS_BUTTONS.keys():
                await self.bot_methods.send_status_to_horeca(callback.data)
                await self.bot_methods.refresh_user_orders(callback.message, forcibly=True)
                if self.order_index > len(self.user_orders) - 1:
                    self.order_index = len(self.user_orders) - 1
                await self.bot_methods.dialog_with_user()

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message, **kwargs):

            # await self.bot_methods.mock_test(message)
            if kwargs.get('command'):
                if kwargs['command'].args:
                    print(kwargs['command'].args)
            await self.bot.delete_message(message.chat.id, message.message_id)
            self.order_index = 0
            self.user_orders = []
            # await self.bot.send_message(message.chat.id, f"user id {message.chat.id}")
            await self.bot_methods.start(message)

        @self.dp.message_handler(content_types=['text'])
        async def text_message(message):
            self.user_data['telegram_user_id'] = message.chat.id
            self.user_data['status'] = message.text

            if message.text == ">>":
                await self.bot_methods.refresh_user_orders(message)
                self.order_index += 1
                await self.bot_methods.dialog_with_user()

            if message.text == "<<":
                await self.bot_methods.refresh_user_orders(message)
                self.order_index -= 1
                await self.bot_methods.dialog_with_user()

            if message.text in variables.customer_buttons_status:
                self.user_data['status'] = variables.customer_buttons_status[message.text]
                requests.post(f"{variables.server_domain}{variables.server_status_from_customer}",
                              json=self.user_data)
            else:
                await self.bot.delete_message(message.chat.id, message.message_id)



        executor.start_polling(self.dp, skip_updates=True)

    async def customer_custom_send_message(self, data):
        self.user_data = data
        user_id = data['telegram_user_id']
        status_text = await self.get_text_from_status_data(data)
        # status_text = f"{variables.status_text_customer}{data['id_order']}: {data['status']}"
        try:
            await self.bot.send_message(user_id, status_text)
        except Exception as ex:
            await self.bot.send_message(int(data['telegram_horeca_id']), f"Пользователь не получил уведомление по причине {str(ex)}")

    async def get_text_from_status_data(self, data) -> str:
        text = f"СТАТУС: {data['status'].capitalize()}\n\n"
        text += f"ЗАКАЗ №{data['order_id']}\n"
        text += f"{data['order_description']}" if type(data['order_description']) is str else ", ".join(data['order_description'])
        return text

    async def check_subscriber(self, user_id):
        try:
            msg = await self.bot.send_message(int(user_id), "Вы можете отслеживать Ваш заказ в этом боте")
            self.user_data['bot_subscribing'] = True
            await msg.delete()
            return True
        except:
            self.user_data['bot_subscribing'] = False
            return False

    # async def start(self, message):
    #     response = requests.get(variables.server_domain + variables.user_info + f"/?telegram_user_id={message.chat.id}")
    #     user_oders = json.loads(response.content.decode('utf-8'))['response']
    #     if not user_oders:
    #         await self.bot_methods.verify_user(message)
    #     elif len(user_oders) > 0 and user_oders[0]['telegram_user_id']:
    #         response = await self.bot_methods.dialog_with_user(message, user_oders)
    #         self.order_index = response['order_index']
    #         self.user_orders = response['user_orders']
    #     else:
    #         print("Something is wrong")
    #         await self.bot.send_message(message.chat.id, "Something is wrong")

    async def bot_name(self):
        bot_name = await self.bot.get_me()
        print("BOT_NAME", bot_name)


