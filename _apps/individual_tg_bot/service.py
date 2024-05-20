import datetime
from typing import Dict

from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.db import AsyncPGDatabase

from _apps.individual_tg_bot.text import suit_vacancies
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from settings.os_getenv import db_url
from _apps.individual_tg_bot.text import all_format, fulltime, remote, office, hybrid

db = AsyncPGDatabase(db_url)


async def show_summary(query: CallbackQuery, data: Dict) -> None:
    work_format_ = data.get("selected_work_format", [])
    work_format = (
        work_format_
        if all_format not in work_format_
        else [fulltime, remote, office, hybrid]
    )
    result = {
        "user_id": query.from_user.id,
        "direction": str(data.get("selected_direction", [])),
        "specialization": ", ".join(data.get("selected_specializations", [])),
        "level": ", ".join(data.get("selected_level", [])),
        "location": ", ".join(data.get("selected_location", [])),
        "work_format": ", ".join(work_format),
        "keyword": str(data.get("keyword", [])),
        "selected_notification": str(data.get("selected_notification", [])),
    }
    await db.create_table()
    await db.insert_into_data(**result)


async def period_get_vacancy_on_getting_task(bot: Bot):
    """Периодическая задача для получения вакансий по наличию новых"""

    result = await db.get_user_request(
        selected_notification=text.on_getting_notification
    )

    interval = datetime.datetime.now() - datetime.timedelta(
        minutes=text.every_thirty_min
    )
    for rq in result:
        vacancies = db.get_periodical_task_vacancies(
            direction=rq.get("direction"),
            specialization=rq.get("specialization"),
            level=rq.get("level"),
            location=rq.get("location"),
            work_format=rq.get("work_format"),
            keyword=rq.get("keywords"),
            interval=interval,
        )

        if vacancies:
            for vacancy in vacancies:
                message = (suit_vacancies + f"{vacancy.get('title')} {vacancy.get('vacancy_url')}\n")
                await bot.send_message(chat_id=rq.get("user_id"), text=message)


async def period_get_vacancy_per_day_task(bot: Bot):
    """Периодическая задача на формирование дайджеста"""
    result = await db.get_user_request(selected_notification=text.per_day_notification)
    for rq in result:

        base_url = "https://4dev.itcoty.ru/user_digest/"

        link = (
            base_url + "?" + "&".join([f"{key}={value}" for key, value in rq.items()])
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Перейти к вакансиям", url=link))
        await bot.send_message(
            chat_id=rq.get("user_id"),
            text=text.per_day_notification,
            reply_markup=keyboard,
        )
