from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.keyboards.inline.direction_buton import (
    get_direction_button,
)
from _apps.individual_tg_bot.keyboards.inline.main_menu import get_inline_menu
from _apps.individual_tg_bot.service import db
from aiogram.types import CallbackQuery


async def reset_request_callback(query: CallbackQuery):
    """Обработка reset_request callback"""
    await db.delete_user_request(query.from_user.id)
    await query.message.answer(text=text.direction, reply_markup=get_direction_button())


async def comeback_request_callback(query: CallbackQuery):
    """Обработка come_back callback"""
    await query.message.answer(
        text.greet.format(name=query.from_user.full_name),
        reply_markup=get_inline_menu(),
    )
