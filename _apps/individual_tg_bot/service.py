import datetime
from urllib.parse import quote
import aiohttp
from _apps.individual_tg_bot import text

from _apps.individual_tg_bot.text import suit_vacancies
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from settings.os_getenv import db_url
from _apps.individual_tg_bot.text import all_format, fulltime, remote, office, hybrid
from _apps.itcoty_web.itcoty_web.settings import URL_USER_REQUEST, URL_VACANCY_TO_TG


async def send_post_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.text()


async def send_get_request(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def send_delete_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.delete(url):
            return None


async def get_user_request(user_id=None, data_id=None, selected_notification=None):
    if user_id:
        params = {'user_id': user_id}
    elif data_id:
        params = {'data_id': data_id}
    elif selected_notification:
        params = {'selected_notification': selected_notification}
    else:
        params = None

    result_all = await send_get_request(URL_USER_REQUEST, params=params)
    return result_all


async def period_get_vacancy_on_getting_task(bot: Bot):
    """Периодическая задача для получения вакансий по наличию новых"""
    interval = datetime.datetime.now() - datetime.timedelta(
        minutes=text.every_thirty_min
    )
    result_all = await get_user_request(selected_notification=text.on_getting_notification)
    base_url = URL_VACANCY_TO_TG

    if result_all:
        for result in result_all.get('results'):
            result['interval'] = interval
            link = (base_url + "?" + quote("&".join([f"{key}={value}" for key, value in result.items()])))
            vacancies = await send_get_request(url=link)
            if vacancies:
                for vacancy in vacancies:
                    message = (suit_vacancies + f"{vacancy.get('title')} {vacancy.get('vacancy_url')}\n")
                    await bot.send_message(chat_id=result.get("user_id"), text=message)


async def period_get_vacancy_per_day_task(bot: Bot):
    """Периодическая задача на формирование дайджеста"""
    result_all = await get_user_request(selected_notification=text.per_day_notification)
    if result_all:
        for result in result_all.get('results'):
            base_url = URL_VACANCY_TO_TG
            link = (base_url + "?" + quote("&".join([f"{key}={value}" for key, value in result.items()])))
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Перейти к вакансиям", url=link))
            await bot.send_message(
                chat_id=result.get("user_id"),
                text=text.per_day_notification,
                reply_markup=keyboard,
            )
