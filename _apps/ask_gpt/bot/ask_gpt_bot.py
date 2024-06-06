import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from _apps.ask_gpt.bot.bot_menu import set_default_commands
from _apps.ask_gpt.bot.variables import chat_gpt_sales_manager as sales_manager_mode, chat_gpt_without_history as without_history_mode
from _apps.ask_gpt.gpt import ask_gpt

config = configparser.ConfigParser()
config.read("./_apps/ask_gpt/settings/config.ini")
token = config['BOT']['token']

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dialog = {}
bot_mode = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Hey')
    await set_config_variables(message)
    await without_history_mode_func(message)

@dp.message_handler(commands=[sales_manager_mode])
async def chat_gpt_sales_manager(message: types.Message):
    await sales_manager_mode_func(message)

@dp.message_handler(commands=[without_history_mode])
async def chat_gpt_without_history(message: types.Message):
    await without_history_mode_func(message)

@dp.message_handler(content_types=['text'])
async def get_text(message: types.Message):
    await set_config_variables(message)
    dialog[message.chat.id].append(message.text)
    if bot_mode[message.chat.id][without_history_mode]:
        actual_dialogue = ask_gpt.actual_dialog(message, dialog[message.chat.id], length=0, prompt=False)
    else:
        actual_dialogue = ask_gpt.actual_dialog(message, dialog[message.chat.id], length=10, prompt=True)
    dialog[message.chat.id].append(ask_gpt.send_request_USA_server(actual_dialogue))
    await bot.send_message(message.chat.id, dialog[message.chat.id][-1], parse_mode='html')

async def set_config_variables(message):
    if not bot_mode.get(message.chat.id):
        bot_mode[message.chat.id] = {
            sales_manager_mode: False,
            without_history_mode: True
        }
    if not dialog.get(message.chat.id):
        dialog[message.chat.id] = []

async def without_history_mode_func(message):
    bot_mode[message.chat.id] = {
        sales_manager_mode: False,
        without_history_mode: True
    }
    dialog[message.chat.id] = []
    await bot.send_message(message.chat.id, text="I can answer without dialog history. Ask me")

async def sales_manager_mode_func(message):
    bot_mode[message.chat.id] = {
        sales_manager_mode: True,
        without_history_mode: False
    }
    dialog[message.chat.id] = []
    await bot.send_message(message.chat.id, text="I'm a sales manager with our dialog history. Ask me")


async def on_startup(dp):
    await set_default_commands(dp.bot)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
