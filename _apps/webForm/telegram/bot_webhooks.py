import asyncio
import logging
import random
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from telegram import variables
from telegram.bot_helper import HelperBot

TOKEN = "6784209473:AAESK6fiESV_ijnf22gwFKBGwiNG9-dalkc"
WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 3001
WEBHOOK_PATH = "/webhook"
EXTERNAL_WEBHOOK_PATH = variables.external_web_hook
WEBHOOK_SECRET = "my-secret"
BASE_WEBHOOK_URL = variables.bot_domain
router = Router()


class WebhookBot:

    def __init__(self):
        self.variables = variables
        self.helper = HelperBot(bot_class=self)

    def main(self) -> None:
        self.dp = Dispatcher()
        self.dp.include_router(router)
        self.dp.startup.register(self.on_startup)
        self.bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
        app = web.Application()
        app.router.add_post(EXTERNAL_WEBHOOK_PATH, self.handle_external_data)

        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=self.dp,
            bot=self.bot,
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, self.dp, bot=self.bot)
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

    async def on_startup(self) -> None:
        path = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
        print("WEBHOOK_PATH=", path)
        await self.bot.set_webhook(
            path,
        )
        @router.message(CommandStart())
        async def command_start_handler(message: Message) -> None:
            await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
            print("your user id:", message.chat.id)
            if message.chat.id not in variables.admins_user_id:
                await self.bot.send_message(message.chat.id, "You have not permissions to use this bot")
            else:
                markup = await self.helper.replyMarkupBuilder(*variables.bar_buttons_start)
                await self.bot.send_message(message.chat.id, f"hello, this bot helps to works with your forms",
                                            reply_markup=markup)

        @router.message(F.text)
        async def text_handler(message: Message) -> None:
            if message.text in variables.bar_buttons_start:
                match message.text:
                    case "Excel":
                        excel_path = await self.helper.send_form_excel()
                        await self.helper.send_file(message, excel_path)

        # @router.message()
        # async def echo_handler(message: types.Message) -> None:
        #     try:
        #         await message.send_copy(chat_id=message.chat.id)
        #     except TypeError:
        #         await message.answer("Nice try!")

    async def handle_external_data(self, request: web.Request):
        data = await request.json()
        if "name" not in data.keys():
            data['name'] = "-"
        text = await self.helper.text_object_from_form(data)
        for id in variables.admins_user_id:
            await self.bot.send_message(id, text)
            await asyncio.sleep(random.randrange(1, 4))
        return web.Response(status=200, text="text was delivered")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot2 = WebhookBot()
    bot2.main()
