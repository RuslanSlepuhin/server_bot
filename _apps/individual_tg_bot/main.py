import asyncio
import logging


from _apps.individual_tg_bot.commands import set_default_commands
from _apps.individual_tg_bot.handlers.main_handler import Handlers
from _apps.individual_tg_bot.service import (
    period_get_vacancy_on_getting_task,
    period_get_vacancy_per_day_task,
)
from _apps.individual_tg_bot.settings import TOKEN
from _apps.individual_tg_bot.text import every_thirty_min, once_per_day
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.types.message import ParseMode
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler


bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
Handlers(dp)
scheduler = AsyncIOScheduler()


@scheduler.scheduled_job("interval", minutes=once_per_day)
async def digest_task():
    await period_get_vacancy_per_day_task(bot=bot)


@scheduler.scheduled_job("interval", minutes=every_thirty_min)
async def on_getting_task():
    await period_get_vacancy_on_getting_task(bot=bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_default_commands(bot))
    loop.run_until_complete(bot.delete_webhook(drop_pending_updates=True))

    dp.filters_factory.bind(Command)

    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
