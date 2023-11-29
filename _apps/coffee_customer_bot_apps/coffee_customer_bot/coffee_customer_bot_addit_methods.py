from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from _apps.coffee_customer_bot_apps.variables import variables


class FormVerificationCode(StatesGroup):
    code = State()


class CustBotAddMethods:
    def __init__(self, bot):
        self.bot = bot

    def composeReplyKeyboard(self, keys_list:list):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        return keyboard.add(*[KeyboardButton(item) for item in keys_list])

    async def start_dialog_with_user(self, message, status=None):
        bar_keyboard = self.composeReplyKeyboard([variables.USER_STATUS_BUTTONS['canceled_by_user'], ])
        await self.bot.send_message(message.chat.id, "PRESS BUTTON" if not status else status, reply_markup=bar_keyboard)

    async def verify_user(self, message):
        await FormVerificationCode.code.set()
        await self.bot.send_message(message.chat.id, variables.dialog_customer['verification'])

    async def check_start(self, json_response):
        try:
            if json_response['telegram_user_id'] and json_response['status'] not in variables.complete_statuses and json_response['order_id']:
                return True
        except Exception as ex:
            print("error methods 1", ex)
        return False

