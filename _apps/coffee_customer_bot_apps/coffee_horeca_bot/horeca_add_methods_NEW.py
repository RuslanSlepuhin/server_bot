import asyncio
import json
import random

import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo, KeyboardButton
from _apps.coffee_customer_bot_apps.variables import variables

class HorecaBotMethods:

    def __init__(self, main_class):
        self.main_class = main_class

    async def start(self, message):
        # self.main_class.orders = await self.get_data_by_user_id(user_id=self.main_class.user_id)
        print(message.chat.id)
        self.main_class.orders = await self.get_data_by_user_id(user_id=message.chat.id)
        print(self.main_class.orders)
        if not self.main_class.orders:
            return await self.main_class.bot.send_message(message.chat.id, "You have not the active current orders")
        self.main_class.orders_dict = await self.data_by_user_to_dict_by_order_id()
        await self.send_short_cards(message=message)

    async def get_data_by_user_id(self, user_id) -> [list]:
        url = variables.server_domain + variables.get_horeca_info + f"?telegram_horeca_id={user_id}&active=true"
        response = requests.get(url)
        return response.json()
        # return variables.mock_object

    async def data_by_user_to_dict_by_order_id(self, order_list:list=None) -> [dict]:
        orders_dict = {}
        order_list = self.main_class.orders if not order_list else order_list
        for item in order_list:
            orders_dict[item['order_id']] = item
        return orders_dict

    async def send_short_cards(self, **kwargs):
        """
        Send short order card with markup but without description
        :param kwargs: message: types.Message; order: dict (optional)
        :return:
        """
        message = kwargs['message'] if 'message' in kwargs else self.main_class.message_dict
        orders = kwargs['orders'] if 'orders' in kwargs else self.main_class.orders
        order_counter = 0
        for order in orders:
            if order['status'] in variables.BARISTA_STATUS_CHOICES:
                order_counter +=1
                if list(variables.BARISTA_STATUS_CHOICES.keys()).index(order['status']) == 0:
                    buttons = variables.first_short_inline_buttons
                else:
                    buttons = variables.between_short_inline_buttons
                await self.custom_send_edit_message(message=message, text=await self.compose_short_text_from_order(order), buttons=buttons, order_id=order['order_id'])
                await asyncio.sleep(random.randrange(1, 3))
            else:
                print("status is not for sending", order['status'])
        if not order_counter:
            await self.main_class.bot.send_message(message.chat.id, "You have no paid orders")

    async def send_full_cards(self, **kwargs):
        """
        Send full order card with description and markup
        :param kwargs: message: types.Message; order: dict (optional)
        :return:
        """
        message = kwargs['message'] if 'message' in kwargs else self.main_class.message
        orders = kwargs['orders'] if 'orders' in kwargs else self.main_class.orders
        for order in orders:
            buttons = variables.first_extended_inline_buttons if list(variables.BARISTA_STATUS_CHOICES.keys()).index(order['status']) == 0 else variables.between_extended_inline_buttons
            await self.custom_send_edit_message(message=message, text=await self.compose_full_text_from_order(order), buttons=buttons, order_id=order['order_id'])

    async def custom_send_edit_message(self, **kwargs):
        """
        Sends message to bot with text and inline buttons
        :param kwargs: text:str, message:types.Message, buttons:dict
        :return:
        """
        addit_row = variables.addition_inline_buttons if self.main_class.orders_dict[kwargs['order_id']]['status'] == 'placed' else None
        markup = await self.inline_markup(kwargs['buttons'], callback_prefix=kwargs['order_id'], addit_row=addit_row) if 'buttons' in kwargs else None

        if kwargs['order_id'] not in self.main_class.message_dict:
            self.main_class.message_dict[kwargs['order_id']] = await self.main_class.bot.send_message(kwargs['message'].chat.id, kwargs['text'], reply_markup=markup)
        else:
            try:
                self.main_class.message_dict[kwargs['order_id']] = await self.main_class.bot.edit_message_text(chat_id=kwargs['message'].chat.id, message_id=kwargs['message'].message_id, text=kwargs['text'], reply_markup=markup)
            except Exception as ex:
                print(ex)
                await self.main_class.message_dict[kwargs['order_id']].edit_text(text=kwargs['text'], reply_markup=markup)


    async def compose_full_text_from_order(self, order) -> [str]:
        text = f"Заказ №{order['order_id']}\n"
        text += f"Описание: "
        if type(order['order_description']) is list:
            for item in order['order_description']:
                text += f"{item}\n"
        else:
            text += f"{order['order_description']}"
        text += f"Кафе: {order['horeca_name']}\n" if 'horeca_name' in order else "\n"
        text += f"Статус: {order['status']}"
        return text

    async def compose_short_text_from_order(self, order) -> [str]:
        return f"Заказ №: {order['order_id']} | Статус: {order['status']}"

    async def inline_markup(self, buttons:dict[str, str], callback_prefix:str, addit_row=None, row_quantity=3):
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
        order_id = kwargs['callback_data'].split("|")[0]
        orders = self.main_class.orders_dict if self.main_class.orders_dict else await self.data_by_user_to_dict_by_order_id(order_list=self.main_class.orders)
        kwargs['orders'] = orders
        kwargs['order_id'] = order_id

        if 'cancel' in kwargs and type(kwargs['cancel']) is bool and kwargs['cancel']:
            await self.main_class.message_dict[order_id].delete()
            self.main_class.message_dict.pop(order_id)
            self.main_class.orders_dict[order_id]['status'] = kwargs['status_value']
            await self.send_status_from_horeca(order_id=order_id)
            self.main_class.orders_dict.pop(order_id)
            return {'message': 'order was deleted'}

        if 'close_order' in kwargs and kwargs['close_order']:
            status = kwargs['status_value'] if 'status_value' in kwargs else kwargs['callback_data'].split("|")[1]
            self.main_class.orders_dict[order_id]['status'] = status
            return await self.send_status_from_horeca(order_id=order_id)

        if 'next_status' in kwargs and type(kwargs['next_status']) is bool:
            status = self.main_class.orders_dict[order_id]['status']
            print(status)
            statuses = list(variables.BARISTA_STATUS_CHOICES.keys())
            index = statuses.index(status)
            if index < len(statuses) + 1:
                status = statuses[index + 1]
                if status in variables.complete_statuses:
                    return await self.set_confirm_data(message=kwargs['message'], callback_data=f"{kwargs['callback_data'].split('|')[0]}|{status}")
                else:
                    self.main_class.orders_dict[order_id]['status'] = status
                    await self.send_status_from_horeca(order_id=order_id)

            # if status in variables.complete_statuses:
            #     await self.set_confirm_data(message=kwargs['message'], callback_data=f"{kwargs['callback_data'].split('|')[0]}|{status}")
            #     # confirm_keyboard = await self.confirm_action_keyboard(prefix=status)
            #     # await self.main_class.bot.send_message(kwargs['message'].chat.id, 'confirm', reply_markup=confirm_keyboard)
            #     # await self.complete_the_order(order_id)
            #     return await self.send_updated_card(kwargs)


        if 'previous_status' in kwargs and type(kwargs['previous_status']) is bool:
            status = self.main_class.orders_dict[order_id]['status']
            print(status)
            statuses = list(variables.BARISTA_STATUS_CHOICES.keys())
            index = statuses.index(status)
            if index > 0:
                status = statuses[index - 1]
                self.main_class.orders_dict[order_id]['status'] = status
            await self.send_status_from_horeca(order_id=order_id)

        if 'status_value' in kwargs and type(kwargs['status_value']) is str:
            self.main_class.orders_dict[order_id]['status'] = kwargs['status_value']
            await self.send_status_from_horeca(order_id=order_id)

        return await self.send_updated_card(kwargs)
        # if 'small_size' in kwargs and type(kwargs['small_size']) is bool and not kwargs['small_size']:
        #     await self.send_full_cards(message=kwargs['message'], orders=[orders[order_id]])
        # else:
        #     await self.send_short_cards(message=kwargs['message'], orders=[orders[order_id]])
        # return {'message': 'order message was sent'}

    async def send_updated_card(self, kwargs):
        if 'small_size' in kwargs and type(kwargs['small_size']) is bool and not kwargs['small_size']:
            await self.send_full_cards(message=kwargs['message'], orders=[kwargs['orders'][kwargs['order_id']]])
        else:
            await self.send_short_cards(message=kwargs['message'], orders=[kwargs['orders'][kwargs['order_id']]])
        return {'message': 'order message was sent'}


    async def send_status_from_horeca(self, **kwargs):
        """

        :param kwargs: order_id: str; status: str (optional: custom)
        :return:
        """
        order = self.main_class.orders_dict[kwargs['order_id']]
        url = variables.server_domain + variables.server_status_from_horeca + f"{kwargs['order_id']}/"
        print(url)
        response = requests.put(url, json=order)
        pass

    async def confirm_action_keyboard(self, prefix):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        yes = types.KeyboardButton(text="Yes", callback_data=prefix + "|yes")
        no = types.KeyboardButton(text="No", callback_data=prefix + "|no")
        return keyboard.row(yes, no)

    async def set_confirm_data(self, message, callback_data):
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
            self.main_class.confirm_message['message'] = await self.main_class.bot.send_message(message.chat.id, text, reply_markup=keyboard)
            self.main_class.confirm_message['callback_data'] = callback_data
        except Exception as ex:
            print('confirm_action_keyboard', ex)
            pass

    async def reset_confirm_data(self):
        await self.main_class.confirm_message['message'].delete()
        self.main_class.confirm_message = {}
        return True

    async def complete_the_order(self, order_id=None):
        order_id = self.main_class.confirm_message['callback_data'].split("|")[0] if not order_id else order_id
        self.main_class.orders_dict.pop(order_id)
        await self.main_class.message_dict[order_id].delete()
        self.main_class.message_dict.pop(order_id)

    async def webAppKeyboard(self):  # создание клавиатуры с webapp кнопкой
        keyboard = ReplyKeyboardMarkup(row_width=1)  # создаем клавиатуру
        webAppInfo = types.WebAppInfo(url="https://google.com")
        button = types.KeyboardButton(text="Open Web App", web_app=webAppInfo)
        button2 = types.KeyboardButton(text="Another Button", callback_data="another_button")
        keyboard.add(button, button2)  # добавляем кнопки в клавиатуру

        return keyboard  # возвращаем клавиатуру
