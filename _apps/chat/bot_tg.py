import asyncio
import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from _apps.chat.chat import Chat

config = configparser.ConfigParser()
config.read("./_apps/chat/settings/config.ini")

class ChatBot:


    def __init__(self):
        self.token = config['Bot']['token']
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.chat = Chat()
        self.request = ""

    def bot_handlers(self):

        class FormVerificationCode(StatesGroup):
            code = State()

        @self.dp.message_handler(state=FormVerificationCode.code)
        async def process_api_id(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['code'] = message.text
                self.request = message.text
            await state.finish()
            answer = self.chat.get_answer(self.request)
            await self.bot.send_message(message.chat.id, answer)
            await dialog(message)

        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await dialog(message)
            pass

        @self.dp.message_handler(content_types=['text'])
        async def text_message(message):
            answer = self.chat.get_answer(message.text)

            await self.bot.send_message(message.chat.id, answer) if answer else ""
            await dialog(message)

        async def dialog(message):
            await FormVerificationCode.code.set()
            await self.bot.send_message(message.chat.id, "You:")

        executor.start_polling(self.dp, skip_updates=True)

if __name__ == '__main__':
    chatBot = ChatBot()
    chatBot.bot_handlers()

