import asyncio
import json
import random
import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo, KeyboardButton, \
    callback_query
from aiogram.utils.exceptions import MessageNotModified
from _apps.coffee_customer_bot_apps.database import sqlite_management as db
from _apps.coffee_customer_bot_apps.variables import variables
from _debug import debug
from _apps.coffee_customer_bot_apps.database import db_short_methods as db

class HorecaBotMethods:

    def __init__(self, main_class):
        self.main_class = main_class

    async def start(self, message) -> bool:
        # utm_bot = message.text.split(' ')[1] if message.text else None
        print('start has been pressed')

        self.main_class.orders[message.chat.id] = await self.get_data_by_user_id(user_id=message.chat.id)
        if not self.main_class.orders[message.chat.id]:
            self.main_class.service_messages[message.chat.id].append(await self.main_class.bot.send_message(message.chat.id, "You have not the active current orders"))
            return False
        self.main_class.orders_dict[message.chat.id] = await self.data_by_user_to_dict_by_order_id(message=message)
        await self.send_short_cards(message=message)
        await self.delete_messages(message=message)
        return True

    async def get_data_by_user_id(self, user_id) -> list:
        url = variables.server_domain + variables.get_horeca_info + f"?telegram_horeca_id={user_id}&active=true"
        print(url)
        response = requests.get(url)
        print("GET ORDERS FROM SERVER from get_data_by_user_id")
        for element in response.json():
            print(f"Заказ: {element['order_id']}\nСтатус: {element['status']}\n-----")
        return response.json()

    async def data_by_user_to_dict_by_order_id(self, order_list:list=None, **kwargs) -> dict:
        chat_id = kwargs['chat_id'] if kwargs.get('chat_id') else kwargs['message'].chat.id
        orders_dict = {}
        order_list = self.main_class.orders[chat_id] if not order_list else order_list
        for item in order_list:
            try:
                orders_dict[item['order_id']] = item
            except Exception as ex:
                print(f"data_by_user_to_dict_by_order_id: {ex}")
                pass
        return orders_dict

    async def send_short_cards(self, **kwargs) -> None:
        """
        Send short order card with markup but without description
        :param kwargs: message: types.Message; order: dict (optional)
        :return:
        """
        chat_id = kwargs['chat_id'] if 'chat_id' in kwargs else kwargs['message'].chat.id
        orders = kwargs['orders'] if 'orders' in kwargs else self.main_class.orders[chat_id]
        

        order_counter = 0
        if debug:
            orders = orders[:5]
        for order in orders:
            if not order.get('status'):
                order['status'] = 'payment_process'
            if order['status'] in variables.BARISTA_STATUS_CHOICES:
                order_counter +=1
                if list(variables.BARISTA_STATUS_CHOICES.keys()).index(order['status']) == 0:
                    buttons = variables.first_short_inline_buttons
                else:
                    buttons = variables.between_short_inline_buttons
                text = await self.compose_short_text_from_order(order)
                if not self.main_class.message_dict[chat_id].get(order['order_id']) or self.main_class.message_dict[chat_id][order['order_id']].text != text:
                    pass
                    await self.custom_send_edit_message(chat_id=chat_id, text=text, buttons=buttons, order_id=order['order_id'])
                    await asyncio.sleep(random.randrange(1, 3))
            else:
                print("status is not for sending", order['order_indicator'])
        if not order_counter:
            self.main_class.service_messages[chat_id].append(await self.main_class.bot.send_message(chat_id, "You have no paid orders"))

    async def send_full_cards(self, **kwargs) -> None:
        """
        Send full order card with description and markup
        :param kwargs: message: types.Message; order: dict (optional)
        :return:
        """
        message = kwargs['message']
        orders = kwargs['orders'] if 'orders' in kwargs else self.main_class.orders[message.chat.id]
        for order in orders:
            buttons = variables.first_extended_inline_buttons if list(variables.BARISTA_STATUS_CHOICES.keys()).index(order['status']) == 0 else variables.between_extended_inline_buttons
            await self.custom_send_edit_message(message=message, text=await self.compose_full_text_from_order(order), buttons=buttons, order_id=order['order_id'])

    async def custom_send_edit_message(self, **kwargs) -> None:
        """
        Sends message to bot with text and inline buttons
        :param kwargs: text:str, message:types.Message, buttons:dict
        :return:
        """
        chat_id = kwargs['chat_id'] if kwargs.get('chat_id') else kwargs['message'].chat.id
        addit_row = variables.addition_inline_buttons if self.main_class.orders_dict[chat_id][kwargs['order_id']]['status'] == 'placed' else None
        markup = await self.inline_markup(kwargs['buttons'], callback_prefix=kwargs['order_id'], addit_row=addit_row) if 'buttons' in kwargs else None

        if kwargs['order_id'] not in self.main_class.message_dict[chat_id]:
            # self.main_class.message_dict[kwargs['order_id']] = await self.main_class.bot.send_message(chat_id, kwargs['text'], reply_markup=markup)
            print("chat_id", chat_id, type(chat_id))
            print("text", kwargs['text'], type(kwargs['text']))
            # print("markup", str(markup), type(markup))
            text = kwargs['text']
            self.main_class.message_dict[chat_id][kwargs['order_id']] = await self.main_class.bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        else:
            try:
                message_id=kwargs['message'].message_id if kwargs.get('message') else self.main_class.message_dict[chat_id][kwargs['order_id']].message_id
                current_message = self.main_class.message_dict[chat_id][kwargs['order_id']]
                if current_message.text != kwargs['text'] or current_message.reply_markup != markup or current_message.chat.id != chat_id:
                    self.main_class.message_dict[chat_id][kwargs['order_id']] = await self.main_class.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=kwargs['text'], reply_markup=markup)
            except MessageNotModified as ex:
                print(f"horeca_add_methods_NEW: custom_send_edit_message: MessageNotModified -> {ex}")
                await self.main_class.message_dict[chat_id][kwargs['order_id']].edit_text(text=kwargs['text'], reply_markup=markup)
            except Exception as ex:
                print(f"horeca_add_methods_NEW: custom_send_edit_message: Exception -> {ex}")
                pass
                # await self.main_class.message_dict[chat_id][kwargs['order_id']].edit_text(text=kwargs['text'], reply_markup=markup)

    async def compose_full_text_from_order(self, order) -> str:
        text = f"Заказ №{order['order_id']}\n"
        text += f"Описание: "
        if type(order['order_description']) is list:
            for item in order['order_description']:
                if type(item) != dict:
                    text += f"{item}\n"
                elif item.items():
                    for key, value in item.items():
                        if item[key]:
                            text += f"{key}: {item[key]}\n"
                    # text += "\n".join(f"{k}: {v}" for k, v in item.items())
                else:
                    pass
        else:
            text += f"{order['order_description']}"

        text_cafe = f"Кафе: {order['horeca_name']}\n" if 'horeca_name' in order else "\n"
        text_status = f"Статус: {order['status']}"

        if len(text + text_cafe + text_status) > 4096:
            text = text[:4096 - len(text_cafe + text_status) - 4]
            text = f"{text}...\n{text_cafe}{text_status}"
        return text

    async def compose_short_text_from_order(self, order) -> str:
        return f"Заказ №: {order['order_id']} | Статус: {order['status']}"

    async def inline_markup(self, buttons:dict[str, str], callback_prefix:str, addit_row=None, row_quantity=3) -> InlineKeyboardMarkup:
        buttons_list = []
        inline_markup = InlineKeyboardMarkup()
        [buttons_list.append(InlineKeyboardButton(key, callback_data=f"{callback_prefix}|{buttons[key]}")) for key in buttons]
        # self.main_class.callbacks = list(buttons.values())
        [inline_markup.add(*buttons_list[i:i + row_quantity]) for i in range(0, len(buttons_list), row_quantity)]
        if addit_row:
            [inline_markup.add(InlineKeyboardButton(key, callback_data=f"{callback_prefix}|{addit_row[key]}")) for key in addit_row]
        return inline_markup

    async def change_card_visual(self, **kwargs):
        """
        It changes the order card visual
        :param kwargs:
            order_id: str;
            message: types.Message
            callback_data:str,
            small_size: bool (optional);
            cancel: bool (optional);
            next_status:bool (optional),
            previous_status: bool (optional)
            status_value: str (optional)
            close_order: bool (optional)
        :return:
        """

        message = kwargs['message']
        chat_id = message.chat.id
        order_id = kwargs['callback_data'].split("|")[0]

        if not self.main_class.orders:
            self.main_class.message_dict[chat_id].append(await self.main_class.bot.send_message(message.chat.id, text='------------------'))
            await self.set_vars(message=message)
            await self.start(message=message)

        orders = self.main_class.orders_dict[chat_id] if self.main_class.orders_dict[chat_id] else await self.data_by_user_to_dict_by_order_id(message=message, order_list=self.main_class.orders[chat_id])
        kwargs['orders'] = orders
        kwargs['order_id'] = order_id

        if 'cancel' in kwargs and type(kwargs['cancel']) is bool and kwargs['cancel']:
            await self.main_class.message_dict[chat_id][order_id].delete()
            self.main_class.message_dict[chat_id].pop(order_id)
            self.main_class.orders_dict[chat_id][order_id]['status'] = kwargs['status_value']
            await self.send_status_from_horeca(message=message,order_id=order_id)
            self.main_class.orders_dict[chat_id].pop(order_id)
            return {'message': 'order was deleted'}

        if 'close_order' in kwargs and kwargs['close_order']:
            status = kwargs['status_value'] if 'status_value' in kwargs else kwargs['callback_data'].split("|")[1]
            self.main_class.orders_dict[chat_id][order_id]['status'] = status
            return await self.send_status_from_horeca(message=message,order_id=order_id)

        if 'next_status' in kwargs and type(kwargs['next_status']) is bool:
            status = self.main_class.orders_dict[chat_id][order_id]['status']
            print(status)
            statuses = list(variables.BARISTA_STATUS_CHOICES.keys())
            index = statuses.index(status)
            if index < len(statuses) + 1:
                status = statuses[index + 1]
                if status in variables.complete_statuses:
                    return await self.set_confirm_data(message=kwargs['message'], callback_data=f"{kwargs['callback_data'].split('|')[0]}|{status}")
                else:
                    self.main_class.orders_dict[chat_id][order_id]['status'] = status
                    await self.send_status_from_horeca(message=message,order_id=order_id)

        if 'previous_status' in kwargs and type(kwargs['previous_status']) is bool:
            status = self.main_class.orders_dict[chat_id][order_id]['status']
            print(status)
            statuses = list(variables.BARISTA_STATUS_CHOICES.keys())
            index = statuses.index(status)
            if index > 0:
                status = statuses[index - 1]
                self.main_class.orders_dict[chat_id][order_id]['status'] = status
            await self.send_status_from_horeca(message=message,order_id=order_id)

        if 'status_value' in kwargs and type(kwargs['status_value']) is str:
            self.main_class.orders_dict[chat_id][order_id]['status'] = kwargs['status_value']
            await self.send_status_from_horeca(message=message,order_id=order_id)

        return await self.send_updated_card(kwargs)
        # if 'small_size' in kwargs and type(kwargs['small_size']) is bool and not kwargs['small_size']:
        #     await self.send_full_cards(message=kwargs['message'], orders=[orders[order_id]])
        # else:
        #     await self.send_short_cards(message=kwargs['message'], orders=[orders[order_id]])
        # return {'message': 'order message was sent'}

    async def send_updated_card(self, kwargs) -> dict:
        if 'small_size' in kwargs and type(kwargs['small_size']) is bool and not kwargs['small_size']:
            await self.send_full_cards(message=kwargs['message'], orders=[kwargs['orders'][kwargs['order_id']]])
        else:
            await self.send_short_cards(message=kwargs['message'], orders=[kwargs['orders'][kwargs['order_id']]])
        return {'message': 'order message was sent'}

    async def send_status_from_horeca(self, **kwargs) -> None:
        """

        :param kwargs: order_id: str; status: str (optional: custom)
        :return:
        """
        message = kwargs['message']
        order = self.main_class.orders_dict[message.chat.id][kwargs['order_id']]
        url = variables.server_domain + variables.server_status_from_horeca + f"{kwargs['order_id']}/"
        print(url)
        response = requests.put(url, json={'status': order['status']})
        pass

    async def confirm_action_keyboard(self, prefix) -> ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        yes = types.KeyboardButton(text="Yes", callback_data=prefix + "|yes")
        no = types.KeyboardButton(text="No", callback_data=prefix + "|no")
        return keyboard.row(yes, no)

    async def set_confirm_data(self, message, callback_data) -> None:
        try:
            status = callback_data.split("|")[1]
            order_id = callback_data.split("|")[0]
            if status in variables.complete_statuses:
                text = f"Подтвердите завершение заказа № {order_id} ⬇️"
            elif status == variables.cancelled_by_cafe_status:
                text = f"Подтвердите отмену заказа № {order_id} ⬇️"
            else:
                text = 'confirm'

            keyboard = await self.confirm_action_keyboard(prefix=callback_data.split("|")[1])
            self.main_class.confirm_message[message.chat.id]['message'] = await self.main_class.bot.send_message(message.chat.id, text, reply_markup=keyboard)
            self.main_class.confirm_message[message.chat.id]['callback_data'] = callback_data
        except Exception as ex:
            print('confirm_action_keyboard', ex)
            pass

    async def reset_confirm_data(self, message) -> bool:
        await self.main_class.confirm_message[message.chat.id]['message'].delete()
        self.main_class.confirm_message[message.chat.id] = {}
        return True

    async def complete_the_order(self, message, order_id=None) -> None:
        order_id = self.main_class.confirm_message[message.chat.id]['callback_data'].split("|")[0] if not order_id else order_id
        self.main_class.orders_dict[message.chat.id].pop(order_id)
        await self.main_class.message_dict[message.chat.id][order_id].delete()
        self.main_class.message_dict[message.chat.id].pop(order_id)

    async def webAppKeyboard(self) -> ReplyKeyboardMarkup:  # создание клавиатуры с webapp кнопкой
        keyboard = ReplyKeyboardMarkup(row_width=1)  # создаем клавиатуру
        webAppInfo = types.WebAppInfo(url="https://google.com")
        button = types.KeyboardButton(text="Open Web App", web_app=webAppInfo)
        button2 = types.KeyboardButton(text="Another Button", callback_data="another_button")
        keyboard.add(button, button2)  # добавляем кнопки в клавиатуру

        return keyboard  # возвращаем клавиатуру

    async def send_enter_key(self, enter_key:dict) -> bool:
        response = requests.post(url=variables.server_domain+variables.send_enterkey_endpoint, json=enter_key)
        print(response.json())
        return True if 400 > response.status_code >= 200 else False

    async def check_available_bot(self, telegram_user_id) -> dict:
        msg = None
        try:
            msg = await self.main_class.bot.send_message(int(telegram_user_id), text="Проверка бота")
        except Exception as ex:
            print(f"send_enter_key: {ex}")
            return {"bot_is_available": False}
        await self.main_class.bot.delete_message(telegram_user_id, msg.message_id)
        return {"bot_is_available": True}

    def print_bot_name(self) -> None:
        bot_name = asyncio.run(self.main_class.bot.get_me())['username']
        print(f"https://t.me/{bot_name}")

    async def async_print_bot_name(self) -> None:
        bot_name = await self.main_class.bot.get_me()
        print(f"https://t.me/{bot_name['username']}")

    async def new_order(self, order:dict) -> dict:
        try:
            print('order:', order)
            user_id = order['telegram_horeca_id']
            await self.set_vars(chat_id=user_id)
            print("NEW_OREDR")
            all = await self.get_all_orders_id(chat_id=user_id)
            if order['order_id'] not in await self.get_all_orders_id(chat_id=user_id):
                orders = order if type(order) is list else [order]
                self.main_class.orders[user_id] = self.main_class.orders[user_id] + orders
                len_new_orders_list = len(orders)

                orders_dict = await self.data_by_user_to_dict_by_order_id(chat_id=user_id, order_list=orders)
                self.main_class.orders_dict[user_id].update(orders_dict)
                user_id = orders[0]['telegram_horeca_id']
                await self.send_short_cards(chat_id=user_id, orders=orders[-len_new_orders_list:])
                response = {'response': order}
            else:
                response = {'response': 'this order id is already in progress'}
            return response

        except Exception as ex:
            print('new_order', ex)
            return {'response': f'Bot error: {str(ex)}'}

    async def get_all_orders_id(self, **kwargs) -> list:
        chat_id = kwargs['chat_id'] if kwargs.get('chat_id') else kwargs['message'].chat.id
        orders_ids_list = []
        for element in self.main_class.orders[chat_id]:
            orders_ids_list.append(element['order_id'])
        return orders_ids_list

    async def notification(self, message: types.Message) -> None:
        not_message = await self.main_class.bot.send_message(message.chat.id, "Обновлено успешно")
        await asyncio.sleep(0,5)
        await not_message.delete()

    async def set_vars(self, **kwargs) -> None:
        chat_id = kwargs['chat_id'] if kwargs.get('chat_id') else kwargs['message'].chat.id
        self.main_class.message_dict[chat_id] = {} if chat_id not in self.main_class.message_dict else self.main_class.message_dict[chat_id]
        self.main_class.orders[chat_id] = [] if chat_id not in self.main_class.orders else self.main_class.orders[chat_id]
        self.main_class.orders_dict[chat_id] = {} if chat_id not in self.main_class.orders_dict else self.main_class.orders_dict[chat_id]
        self.main_class.callbacks[chat_id] = [] if chat_id not in self.main_class.callbacks else self.main_class.callbacks[chat_id]
        self.main_class.confirm_message[chat_id] = {} if chat_id not in self.main_class.confirm_message else self.main_class.confirm_message[chat_id]
        self.main_class.start_message[chat_id] = {} if chat_id not in self.main_class.start_message else self.main_class.start_message[chat_id]
        self.main_class.service_messages[chat_id] = [] if chat_id not in self.main_class.service_messages else self.main_class.service_messages[chat_id]

    async def delete_messages(self, **kwargs):
        chat_id = kwargs['chat_id'] if kwargs.get('chat_id') else kwargs['message'].chat.id
        for i in range(0, len(self.main_class.service_messages[chat_id])):
            try:
                await self.main_class.service_messages[chat_id][i].delete()
            except Exception as ex:
                print(ex)
                pass
        self.main_class.service_messages[chat_id] = []

