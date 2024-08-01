import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import web
from _apps.coffee_customer_bot_apps.variables import variables
from _apps.coffee_customer_bot_apps.coffee_horeca_bot.horeca_add_methods_NEW import HorecaBotMethods
from _apps.coffee_customer_bot_apps.variables.variables import new_order_endpoint, provide_message_to_horeca_endpoint, is_horeca_active_endpoint
from _apps.coffee_customer_bot_apps.coffee_horeca_bot.webhook import WebHoock
from _debug import debug
from _apps.coffee_customer_bot_apps.database import db_short_methods as db
from _apps.coffee_customer_bot_apps.variables import database_variables as db_var

config = configparser.ConfigParser()

path = "./_apps/coffee_customer_bot_apps/settings/config.ini"
print(path)
config.read(path)
token = config['Bot']['horeca_token']
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

ngrok_payload = "9676-178-127-147-229"
WEBHOOK_URL = f"https://{ngrok_payload}.ngrok-free.app" if debug else "https://4dev.itcoty.ru"
WEBHOOK_PATH = '/horeca/wh'
NEW_ORDER_PATH = new_order_endpoint
MESSAGE_FROM_CUSTOMER = provide_message_to_horeca_endpoint
IS_HORECA_ACTIVE = is_horeca_active_endpoint


# db create tables
for key in db_var.tables:
    db.create_tables(query=db_var.tables[key]['create_query'])


class HorecaBot:

    def __init__(self, token=None, bot=None):
        self.__token = token if token else config['Bot']['horeca_token']
        self.bot = Bot(token=self.__token) if not bot else bot
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        Bot.set_current(self.bot)
        self.user_id = None #None
        self.user_data = {}
        self.methods = HorecaBotMethods(self)
        self.webhook_methods = WebHoock(self)

        # self.message_dict = {}
        # self.orders = []
        # self.orders_dict = {}
        # self.callbacks = []
        # self.confirm_message = {}

        self.notification = {}
        self.message_dict = {}
        self.orders = {} #[]
        self.orders_dict = {}
        self.callbacks = {} #[]
        self.confirm_message = {}
        self.start_message = {}
        self.service_messages = {}

    async def on_startup(self, app):
        await self.bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)
        print("Bot has been started")

    async def on_shutdown(self, app):
        print("Bot has been stopped")
        await self.bot.delete_webhook()
        await self.dp.storage.close()
        await self.dp.storage.wait_closed()


    def bot_handlers(self):
        self.methods.print_bot_name()

        app = web.Application()
        app.router.add_post(WEBHOOK_PATH, self.webhook_methods.webhook_handler)
        app.router.add_post(NEW_ORDER_PATH, self.webhook_methods.get_new_order)
        app.router.add_post(MESSAGE_FROM_CUSTOMER, self.webhook_methods.provide_message_from_customer)
        app.router.add_get(IS_HORECA_ACTIVE, self.webhook_methods.is_horeca_active)

        app.on_startup.append(self.on_startup)
        app.on_shutdown.append(self.on_shutdown)

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            enter_key = message.text.split("/start", 1)[1]
            if enter_key:
                response = await self.methods.send_enter_key({"enter_key": enter_key.strip(), "telegram_user_id": message.chat.id})

            await self.methods.set_vars(message=message)
            self.service_messages[message.chat.id].append(await self.bot.send_message(message.chat.id, str(message.chat.id) + f" {variables.updating_message}", reply_markup=types.ReplyKeyboardRemove()))
            self.service_messages[message.chat.id].append(message)
            self.user_id = message.chat.id
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
                    print('self.confirm_message', self.confirm_message)
                    data = self.confirm_message[message.chat.id]['callback_data'].split("|")[1]
                    match data:
                        # case "cancel":
                        #     await self.methods.change_card_visual(message=message, callback_data=self.confirm_message['callback_data'], status_value=variables.cancelled_by_cafe_status, cancel=True)
                        case "canceled_by_cafe":
                            await self.methods.change_card_visual(message=message, callback_data=self.confirm_message[message.chat.id]['callback_data'], status_value=variables.cancelled_by_cafe_status, cancel=True)
                        case "next_status":
                            await self.methods.change_card_visual(message=self.confirm_message[message.chat.id]['message'], callback_data=self.confirm_message[message.chat.id]['callback_data'], next_status=True)
                        case "previous_status":
                            await self.methods.change_card_visual(message=self.confirm_message[message.chat.id]['message'], callback_data=self.confirm_message[message.chat.id]['callback_data'], previous_status=True)
                        case "delivered":
                            await self.methods.change_card_visual(message=self.confirm_message[message.chat.id]['message'], callback_data=self.confirm_message[message.chat.id]['callback_data'], close_order=True)

                    if data in variables.complete_statuses:
                        await self.methods.complete_the_order(message)

                await self.bot.delete_message(message.chat.id, message.message_id)
                await self.methods.reset_confirm_data(message)

        web.run_app(app, host='0.0.0.0', port=4000)
        # executor.start_polling(self.dp, skip_updates=True)

if __name__ == "__main__":
    b = HorecaBot()
    b.bot_handlers()

