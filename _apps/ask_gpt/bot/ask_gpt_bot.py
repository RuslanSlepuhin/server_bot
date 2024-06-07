import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from _apps.ask_gpt.bot.bot_menu import set_default_commands
from _apps.ask_gpt.bot.variables import chat_gpt_sales_manager as sales_manager_mode, \
    chat_gpt_without_history as without_history_mode, chat_gpt_set_prompt, watch_prompt, tokens_number
from _apps.ask_gpt.gpt import ask_gpt
from _debug import debug

config = configparser.ConfigParser()
config.read("./_apps/ask_gpt/settings/config.ini")
token = config['BOT']['token'] #if not debug else config['BOT']['token_debug']

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dialog = {}
bot_mode = {}
prompt_mode = {}
tokens = {}

# --------------------- SET PROMPT ----------------------------

class SetPrompt(StatesGroup):
    prompt = State()

@dp.message_handler(state=SetPrompt.prompt)
async def setPrompt_prompt(message: types.Message, state: FSMContext):
    await set_config_variables(message)
    async with state.proxy() as data:
        data['prompt'] = message.text
        prompt_mode[message.chat.id] = data['prompt']
    await state.finish()
    await bot.send_message(message.chat.id, "👉 prompt has been set")
    await with_history_mode_func(message)

@dp.message_handler(commands=[chat_gpt_set_prompt])
async def chat_gpt_set_prompt(message: types.Message):
    await bot.send_message(message.chat.id, 'Input PROMPT')
    await SetPrompt.prompt.set()

@dp.message_handler(commands=[watch_prompt])
async def watch_set_prompt(message: types.Message):
    await bot.send_message(message.chat.id, f"Your PROMPT:\n{prompt_mode[message.chat.id]}") if prompt_mode.get(message.chat.id) and prompt_mode[message.chat.id] else await bot.send_message(message.chat.id, "You have any PROMPT")
# --------------------- END SET PROMPT ----------------------------

# --------------------- SET TOKENS NUMBER ----------------------------
class SetTokensNumber(StatesGroup):
    tokens_state = State()

@dp.message_handler(state=SetTokensNumber.tokens_state)
async def SetTokensNumber_f(message: types.Message, state: FSMContext):
    await set_config_variables(message)
    async with state.proxy() as data:
        data['tokens_state'] = message.text
        if message.text.isdigit():
            prompt_mode[message.chat.id] = data['tokens']
        else:
            await bot.send_message(message.chat.id, text="Input numbers only")
    await state.finish()
    await bot.send_message(message.chat.id, "👉 tokens number has been set")

@dp.message_handler(commands=[tokens_number])
async def chat_gpt_set_prompt(message: types.Message):
    await set_config_variables(message)
    await bot.send_message(message.chat.id, 'Input tokens number')
    await SetPrompt.prompt.set()

@dp.message_handler(commands=[watch_prompt])
async def watch_set_prompt(message: types.Message):
    await bot.send_message(message.chat.id, f"Your PROMPT:\n{prompt_mode[message.chat.id]}") if prompt_mode.get(message.chat.id) and prompt_mode[message.chat.id] else await bot.send_message(message.chat.id, "You have any PROMPT")
# --------------------- END SET TOKENS NUMBER ----------------------------

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Hey')
    await set_config_variables(message)
    await without_history_mode_func(message)

@dp.message_handler(commands=[sales_manager_mode])
async def chat_gpt_sales_manager(message: types.Message):
    await with_history_mode_func(message)

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
        actual_dialogue = ask_gpt.actual_dialog(message, dialog[message.chat.id], length=10, prompt=True, prompt_text=prompt_mode[message.chat.id])
    dialog[message.chat.id].append(ask_gpt.send_request_USA_server(actual_dialogue, tokens[message.chat.id]))
    await bot.send_message(message.chat.id, dialog[message.chat.id][-1], parse_mode='html')

async def set_config_variables(message):
    if not bot_mode.get(message.chat.id):
        bot_mode[message.chat.id] = {
            sales_manager_mode: False,
            without_history_mode: True
        }
    if not dialog.get(message.chat.id):
        dialog[message.chat.id] = []
    if not prompt_mode.get(message.chat.id):
        prompt_mode[message.chat.id] = ""
    if not tokens.get(message.chat.id):
        tokens[message.chat.id] = 150

async def without_history_mode_func(message):
    bot_mode[message.chat.id] = {
        sales_manager_mode: False,
        without_history_mode: True
    }
    dialog[message.chat.id] = []
    await bot.send_message(message.chat.id, text="I can answer without dialog history. Ask me")

async def with_history_mode_func(message):
    bot_mode[message.chat.id] = {
        sales_manager_mode: True,
        without_history_mode: False
    }
    dialog[message.chat.id] = []
    await bot.send_message(message.chat.id, text="I'll remember our dialog history. Ask me")


async def on_startup(dp):
    await set_default_commands(dp.bot)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
