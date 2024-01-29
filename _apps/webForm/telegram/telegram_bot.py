import asyncio
import configparser
import logging
import os
import random
import sys
import time
from datetime import datetime
from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.markdown import hbold
from telegram import variables

# config = configparser.ConfigParser()
# config.read(".\settings\config.ini")
# token = config["Bot"]["token"]
from telegram.bot_helper import HelperBot




class BotHandlers:

    def __init__(self, **kwargs):
        self.token = kwargs['token']
        self.bot = Bot(token=self.token, parse_mode=ParseMode.HTML)
        self.dp = Dispatcher()
        self.variables = variables
        self.helper = HelperBot(bot_class=self)

    async def handlers(self):
        print("https://t.me/a34fgh6_bot")

        @self.dp.message(CommandStart())
        async def command_start_handler(message: Message) -> None:
            print("your user id:", message.chat.id)
            print(os.getcwd())
            if message.chat.id not in variables.admins_user_id:
                await self.bot.send_message(message.chat.id, "You have not permissions to use this bot")
            else:
                markup = await self.helper.replyMarkupBuilder(*variables.bar_buttons_start)
                await self.bot.send_message(message.chat.id, f"hello, this bot helps to works with your forms", reply_markup=markup)

        @self.dp.message(F.text)
        async def text_handler(message: types.Message) -> None:
            if message.text in variables.bar_buttons_start:
                match message.text:
                    case "Excel":
                        excel_path = await self.helper.send_form_excel()
                        await self.helper.send_file(message, excel_path)

        await self.dp.start_polling(self.bot)

    async def send_message_custom(self, text):
        for admin in variables.admins_user_id:
            await self.bot.send_message(chat_id=admin, text=text)
            await asyncio.sleep(random.randrange(1, 4))


