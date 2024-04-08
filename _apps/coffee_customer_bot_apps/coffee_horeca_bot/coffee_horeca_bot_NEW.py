import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from _apps.coffee_customer_bot_apps.variables import variables
from _apps.coffee_customer_bot_apps.coffee_horeca_bot.horeca_add_methods_NEW import HorecaBotMethods

config = configparser.ConfigParser()
config.read("./_apps./coffee_customer_bot_apps/settings/config.ini")

class HorecaBot:

    def __init__(self, __token=None):
        self.__token = __token if __token else config['Bot']['horeca_token']
        self.bot = Bot(token=self.__token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.user_id = None
        self.user_data = {}
        self.message_dict = {}
        self.methods = HorecaBotMethods(self)
        self.orders = []
        self.orders_dict = {}
        self.callbacks = []
        self.confirm_message = {}

    def bot_handlers(self):

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            enter_key = message.text.split("/start", 1)[1]
            if enter_key:
                response = await self.methods.send_enter_key({"enter_key": enter_key.strip(), "telegram_user_id": message.chat.id})
            self.user_id = message.chat.id
            await self.bot.send_message(message.chat.id, f"Your id is {message.chat.id}")
            await self.methods.start(message)

        @self.dp.callback_query_handler()
        async def callbacks(callback: types.CallbackQuery):
            if callback.data.split("|")[1] in variables.context_menu_list:
                match callback.data.split("|")[1]:
                    case 'maximize': await self.methods.change_card_visual(message=callback.message, small_size=False, callback_data=callback.data)
                    case "next_status":
                        # await self.methods.set_confirm_data(callback.message, callback.data)
                        await self.methods.change_card_visual(message=callback.message, callback_data=callback.data, next_status=True)
                    case "minimize": await self.methods.change_card_visual(message=callback.message, callback_data=callback.data)
                    # case "cancel":
                    #     await self.methods.set_confirm_data(callback.message, callback.data)
                    case "canceled_by_cafe":
                        await self.methods.set_confirm_data(callback.message, callback.data)
                    case "previous_status":
                        # await self.methods.set_confirm_data(callback.message, callback.data)
                        await self.methods.change_card_visual(message=callback.message, callback_data=callback.data, previous_status=True)

        @self.dp.message_handler(content_types=['text'])
        async def text_message(message):

            self.user_data['telegram_user_id'] = message.chat.id
            self.user_data['status'] = message.text

            if message.text in ['Yes', 'No'] and self.confirm_message:
                if message.text == "Yes":
                    data = self.confirm_message['callback_data'].split("|")[1]
                    match data:
                        # case "cancel":
                        #     await self.methods.change_card_visual(message=message, callback_data=self.confirm_message['callback_data'], status_value=variables.cancelled_by_cafe_status, cancel=True)
                        case "canceled_by_cafe":
                            await self.methods.change_card_visual(message=message, callback_data=self.confirm_message['callback_data'], status_value=variables.cancelled_by_cafe_status, cancel=True)
                        case "next_status":
                            await self.methods.change_card_visual(message=self.confirm_message['message'], callback_data=self.confirm_message['callback_data'], next_status=True)
                        case "previous_status":
                            await self.methods.change_card_visual(message=self.confirm_message['message'], callback_data=self.confirm_message['callback_data'], previous_status=True)
                        case "delivered":
                            await self.methods.change_card_visual(message=self.confirm_message['message'], callback_data=self.confirm_message['callback_data'], close_order=True)

                    if data in variables.complete_statuses:
                        await self.methods.complete_the_order()

                await self.bot.delete_message(message.chat.id, message.message_id)
                await self.methods.reset_confirm_data()


        executor.start_polling(self.dp, skip_updates=True)

    async def check_subscriber_horeca(self, telegram_user_id):
        return await self.methods.check_available_bot(telegram_user_id)

