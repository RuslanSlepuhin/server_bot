from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.keyboards.inline.direction_buton import (
    get_direction_button,
)

from _apps.individual_tg_bot.keyboards.inline.new_request import new_request_button
from _apps.individual_tg_bot.keyboards.inline.notifications import (
    change_notification,
)
from _apps.individual_tg_bot.service import db
from aiogram.types import CallbackQuery, ReplyKeyboardRemove


async def get_vacancy_filter(query: CallbackQuery) -> None:
    """Обработка vacancy_filter callback"""
    result = await db.get_user_request(user_id=query.from_user.id)
    if result:
        request = {
            text.chosen_direction: result[0].get("direction"),
            text.chosen_specialization: result[0].get("specialization"),
            text.chosen_level: result[0].get("level"),
            text.chosen_location: result[0].get("location"),
            text.chosen_format: result[0].get("work_format"),
            text.add_info: result[0].get("keywords"),
        }

        user_request = text.user_current_request
        for key, value in request.items():
            user_request += f"{key} {value}\n"

        await query.message.answer(
            text=user_request, reply_markup=ReplyKeyboardRemove()
        )
        await query.message.answer(text.new_request, reply_markup=new_request_button())
    else:
        await query.message.answer(
            text=text.direction, reply_markup=get_direction_button()
        )


async def get_notification_callback(query: CallbackQuery) -> None:
    """Обработка notification callback"""
    result = await db.get_user_request(user_id=query.from_user.id)
    if result:
        selected_notification = result[0].get("selected_notification")
        await query.message.answer(
            text.chosen_notification.format(notification=selected_notification.lower()),
            reply_markup=change_notification(),
        )
    else:
        await query.message.answer(text=text.make_vacancy_filter)
        await query.message.answer(
            text=text.direction, reply_markup=get_direction_button()
        )


async def get_restart_callback(query: CallbackQuery) -> None:
    """Обработка restart callback"""
    await db.delete_user_request(user_id=query.from_user.id)
    await query.message.answer(text=text.success_restart)
    await query.message.answer(text.new_request, reply_markup=new_request_button())
