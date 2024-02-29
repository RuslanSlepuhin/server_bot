import json
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from _apps.coffee_customer_bot_apps.variables import variables
import requests

class FormVerificationCode(StatesGroup):
    code = State()

class CustBotAddMethods:
    def __init__(self, bot, CustomerBot):
        self.bot = bot
        self.CustomerBot = CustomerBot
        self.user_orders = []
        self.order_index = 0
        self.message = None
        self.msg = None

    def composeReplyKeyboard(self, keys_list:list):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        return keyboard.add(*[KeyboardButton(item) for item in keys_list])

    async def start(self, message):
        self.message = message
        response = requests.get(variables.server_domain + variables.user_info + f"?telegram_user_id={self.message.chat.id}")
        if 200 <= response.status_code <= 300:
            response = response.json()
            if not response:
                await self.verify_user()
            elif len(response) > 0 and response[0]['telegram_user_id']:
                await self.refresh_user_orders(message)
                if self.CustomerBot.user_orders:
                    await self.dialog_with_user()
                else:
                    await self.customer_custom_send_message(text=variables.you_have_any_order, keyboard=None)
            else:
                print("Something is wrong")
                await self.bot.send_message(self.message.chat.id, "Something is wrong")
        else:
            await self.bot.send_message(message.chat.id, f"Server is not responding: {str(response.status_code)}\nresponse url: {response.url}")

    async def dialog_with_user(self, user_orders=None, order_index=None):
        self.CustomerBot.user_orders = user_orders if user_orders else self.CustomerBot.user_orders
        if not self.CustomerBot.user_orders:
            return await self.customer_custom_send_message(text=variables.you_have_any_order, keyboard=None)

        if self.CustomerBot.order_index > len(self.CustomerBot.user_orders) - 1:
            self.CustomerBot.order_index -= 1
            return self.CustomerBot.order_index

        self.CustomerBot.order_index = order_index if order_index not in [None, ] else self.CustomerBot.order_index
        text = ''
        keyboard = await self.fuckingReplyKeyboard()

        print(self.CustomerBot.user_orders)

        text += f"ЗАКАЗ: {self.CustomerBot.user_orders[self.CustomerBot.order_index]['order_id']}\n"
        text += f"КОФЕЙНЯ: {self.CustomerBot.user_orders[self.CustomerBot.order_index]['cafe_id__name']}\n"
        text += f"ОПИСАНИЕ ЗАКАЗА: {self.CustomerBot.user_orders[self.CustomerBot.order_index]['order_description']}\n" if type(self.CustomerBot.user_orders[self.CustomerBot.order_index]['order_description']) is str else f"ОПИСАНИЕ ЗАКАЗА: {', '.join(self.CustomerBot.user_orders[self.CustomerBot.order_index]['order_description'])}\n"
        text += f"СТАТУС ЗАКАЗА: {self.CustomerBot.user_orders[self.CustomerBot.order_index]['status']}\n"

        if not keyboard:
            keyboard = ReplyKeyboardRemove()
        await self.customer_custom_send_message(text=text, keyboard=keyboard)

    async def verify_user(self):
        await FormVerificationCode.code.set()
        await self.bot.send_message(self.message.chat.id, variables.dialog_customer['verification'])

    async def check_start(self, json_response):
        try:
            if json_response['telegram_user_id'] and json_response['status'] not in variables.complete_statuses and json_response['order_id']:
                return True
        except Exception as ex:
            print("error methods 1", ex)
        return False

    async def fuckingReplyKeyboard(self, reply_keyboard=False, **kwargs):
        keyboards_list = []

        self.CustomerBot.order_index = kwargs['order_index'] if 'order_index' in kwargs and kwargs['order_index'] else self.CustomerBot.order_index
        self.CustomerBot.user_orders = kwargs['user_orders'] if 'user_orders' in kwargs and kwargs['user_orders'] else self.CustomerBot.user_orders

        if reply_keyboard:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            if self.CustomerBot.user_orders[self.CustomerBot.order_index]['status'] in variables.USER_STATUSES_CANCEL_IMPOSSIBLE:
                keyboard.add("canceled_by_user")
            keyboards_list.append("<<") if self.CustomerBot.order_index>0 else keyboards_list.append("|")
            keyboards_list.append(f"{self.CustomerBot.order_index + 1}| {len(self.CustomerBot.user_orders)}")
            keyboards_list.append(">>") if self.CustomerBot.order_index<len(self.CustomerBot.user_orders) - 1 else keyboards_list.append("|")
            keyboard.add(*keyboards_list)
        else:
            keyboard = InlineKeyboardMarkup(resize_keyboard=True)
            if self.CustomerBot.user_orders[self.CustomerBot.order_index]['status'] in variables.USER_STATUSES_CANCEL_IMPOSSIBLE:
                keyboard.add(InlineKeyboardButton("canceled_by_user", callback_data="canceled_by_user"))
            keyboards_list.append(InlineKeyboardButton("<<", callback_data="<<")) if self.CustomerBot.order_index>0 else keyboards_list.append(InlineKeyboardButton("|", callback_data="!"))
            keyboards_list.append(InlineKeyboardButton(f"{self.CustomerBot.order_index + 1}| {len(self.CustomerBot.user_orders)}", callback_data="!"))
            keyboards_list.append(InlineKeyboardButton(">>", callback_data=">>")) if self.CustomerBot.order_index<len(self.CustomerBot.user_orders) - 1 else keyboards_list.append(InlineKeyboardButton("|", callback_data="!"))
            keyboard.add(*keyboards_list)

        return keyboard

    async def refresh_user_orders(self, message, forcibly=False):
        self.message = message if not self.message else self.message
        if forcibly:
            self.CustomerBot.user_orders = await self.get_users_info(message)
        else:
            if not self.CustomerBot.user_orders:
                self.CustomerBot.user_orders = await self.get_users_info(message)

    async def get_users_info(self, message):
        conditions = f"?telegram_user_id={message.chat.id}&active=true"
        response = requests.get(variables.server_domain + variables.user_info + conditions)
        return response.json()

    async def send_status_to_horeca(self, status):
        order = self.CustomerBot.user_orders[self.CustomerBot.order_index]
        order['status'] = status
        try:
            requests.post(variables.server_domain + variables.server_status_from_customer, json=order)
            return True
        except Exception as ex:
            print(ex)
            return False

    async def customer_custom_send_message(self, text, keyboard):
        if not self.msg:
            self.msg = await self.bot.send_message(self.message.chat.id, text, reply_markup=keyboard)
        else:
            try:
                await self.msg.edit_text(text, reply_markup=keyboard)
            except Exception as ex:
                try:
                    await self.msg.delete()
                except:
                    pass
                self.msg = await self.bot.send_message(self.message.chat.id, text, parse_mode='html',
                                                       reply_markup=keyboard)

    async def mock_test(self, message):
        requests.get(variables.server_domain + f"/mock?telegram_user_id={message.chat.id}")
