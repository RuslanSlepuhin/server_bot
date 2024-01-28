import asyncio
import random
from _apps.web_form_bot import variables
from aiogram import Bot, Dispatcher, types
from aiohttp import web
from _apps.web_form_bot.bot_helper import HelperBot

TOKEN_API = "6784209473:AAESK6fiESV_ijnf22gwFKBGwiNG9-dalkc"
bot = Bot(token=TOKEN_API)
Bot.set_current(bot)
dp = Dispatcher(bot)
app = web.Application()

# webhook_path = f'/{TOKEN_API}'  #
webhook_path = f"/webhook"  #

port = variables.port
host = variables.host
bot_server_host = variables.bot_domain

helper = HelperBot()

def bot_init():
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(
        app,
        host=host,
        port=port
    )

async def set_webhook():
    webhook_uri = f'{bot_server_host}{webhook_path}'
    await bot.set_webhook(
        webhook_uri
    )

async def on_startup(_):
    await set_webhook()
    print('Bot has been started')

async def on_shutdown(_):
    print('Bot has been stopped')

@dp.message_handler(commands=['start', 'help'])
async def cmd_start_help(message: types.Message) -> None:
    await message.answer(f"Hello, {(message.from_user.full_name)}!")
    print("your user id:", message.chat.id)
    if message.chat.id not in variables.admins_user_id:
        await bot.send_message(message.chat.id, "You have not permissions to use this bot")
    else:
        markup = await helper.replyMarkupBuilder(*variables.bar_buttons_start)
        await bot.send_message(message.chat.id, f"hello, this bot helps to works with your forms", reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def content_type_text(message: types.Message):
    if message.text in variables.bar_buttons_start:
        match message.text:
            case "Excel":
                excel_path = await helper.send_form_excel()
                if excel_path:
                    await helper.send_file(message, excel_path)
                else:
                    print("Server is not connection")


async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index + 1:]
    if token == "webhook":
        update = types.Update(**await request.json())
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)

async def external_post(request):
    data = await request.json()
    print(data)
    if "name" not in data.keys():
        data['name'] = "-"
    text = await helper.text_object_from_form(data)
    for id in variables.admins_user_id:
        await bot.send_message(id, text)
        await asyncio.sleep(random.randrange(1, 4))
    return web.Response(status=200, text="text was delivered")


app.router.add_post(f"/webhook", handle_webhook)
app.router.add_post('/external', external_post)



if __name__ == "__main__":
    bot_init()