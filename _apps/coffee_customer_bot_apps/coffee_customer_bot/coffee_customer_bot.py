import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from coffee_customer_bot_apps.variables import variables
from coffee_customer_bot_apps.coffee_customer_bot.coffee_customer_bot_addit_methods import CustBotAddMethods
from coffee_customer_bot_apps.coffee_customer_bot.coffee_customer_bot_addit_methods import FormVerificationCode
from coffee_customer_bot_apps.database.database_methods import DataBase

config = configparser.ConfigParser()
config.read("./coffee_customer_bot_apps/settings/config.ini")

class CustomerBot:
    def __init__(self, token=None):
        self.token = token if token else config['Bot']['customer_token']
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.test_data = {'user_id': 648154559, 'id_horeca': 3, 'id_order': '7fa99e', 'status': 'canceled_by_user'}
        self.bot_methods = CustBotAddMethods(bot=self.bot)
        self.user_data = variables.user_data
        self.database_methods = DataBase()

    def bot_handlers(self):

        @self.dp.message_handler(state=FormVerificationCode.code)
        async def process_api_id(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['code'] = message.text
                self.user_data['verification_code'] = message.text
            await state.finish()
            response = requests.post(variables.server_domain + variables.verification_endpoint, self.user_data)
            if not response:
                await self.bot.send_message(message.chat.id, variables.dialog_customer['verification_error'])
                await self.bot_methods.verify_user(message)
            else:
                await self.bot_methods.start_dialog_with_user(message)


        @self.dp.message_handler(commands=['get_users'])
        async def get_users(message: types.Message):
            pass

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            self.user_data['telegram_user_id'] = message.chat.id
            self.user_data['bot_subscribing'] = True
            self.user_data['verification_code'] = self.user_data['verification_code'] if 'verification_code' in self.user_data else ""


            # self.database_methods.connect()
            # self.database_methods.db_execute(variables.database_user_create_table, "done")
            # self.database_methods.insert_data(self.user_data)

            # request to get user info user_id and verification code
            # if user_id and verification code ->
                # request order status
                # and show it for user
            # elif not user_id and verification code
                # send input the verification code
                # requests.post({user_id, verification code})
            # else
                # do nothing


            if self.user_data['telegram_user_id'] and self.user_data['verification_code']:
                await self.bot_methods.start_dialog_with_user(message)
            elif not self.user_data['verification_code']:
                await self.bot_methods.verify_user(message)
            else:
                await self.bot.send_message(message.chat.id, "Something is damage in START method. Looking for errors there")

        @self.dp.callback_query_handler()
        async def callbacks(callback: types.CallbackQuery):
            pass

        @self.dp.message_handler(content_types=['text'])
        async def text_message(message):
            self.test_data['telegram_user_id'] = message.chat.id
            self.test_data['status'] = message.text

            if message.text in variables.customer_buttons_status:
                self.user_data['status'] = variables.customer_buttons_status[message.text]
                requests.post(f"{variables.server_domain}{variables.server_test_status_endpoint_from_customer}",
                              json=self.test_data)

            else:
                await self.bot.delete_message(message.chat.id, message.message_id)

        executor.start_polling(self.dp, skip_updates=True)



    async def custom_send_message(self, data):
        user_id = data['telegram_user_id']
        await self.bot.send_message(user_id, str(data))

    async def check_subscriber(self, user_id):
        try:
            msg = await self.bot.send_message(int(user_id), "Вы можете отслеживать Ваш заказ в этом боте")
            self.user_data['bot_subscribing'] = True
            await msg.delete()
            return True
        except:
            self.user_data['bot_subscribing'] = False
            return False
