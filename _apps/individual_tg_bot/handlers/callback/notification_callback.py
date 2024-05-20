from urllib.parse import quote

from aiogram.dispatcher import FSMContext

from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.handlers.callback.callback_service import (
    confirm_choice_handler,
    user_digest,
)
from _apps.individual_tg_bot.keyboards.inline.main_menu import get_inline_menu
from _apps.individual_tg_bot.keyboards.inline.notifications import (
    notification_button,
    notification_dict_user,
)
from _apps.individual_tg_bot.service import db, show_summary
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


async def notification_callback_handler(
    query: CallbackQuery, state: FSMContext
) -> None:
    """Обработка callback для уведомления"""
    data = await state.get_data()
    selected_notification = data.get("selected_notification", set())
    await state.update_data(selected_notification=selected_notification)

    if query.data in notification_dict_user:
        await confirm_choice_handler(
            query=query,
            selected_specializations=selected_notification,
            buttons_dict=notification_dict_user,
        )

    data_final = await state.get_data()
    base_url = "https://4dev.itcoty.ru/user_requests_vacancies"
    link = (base_url + "?" + quote("&".join([f"{key}={value}" for key, value in data_final.items()])))
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Перейти к вакансиям", url=link))

    digest = await user_digest(data_final)
    await query.message.answer(text=f"Выбранные критерии:\n{str(digest)}")
    await query.message.answer(text=text.thanks_text, reply_markup=keyboard)
    await query.message.answer(text=text.menu_user)
    await show_summary(query=query, data=data_final)

    await state.finish()


async def get_per_day_notification(query: CallbackQuery) -> None:
    """Обработка per_day_notification callback"""
    await db.change_user_notification(
        notification=text.per_day_notification, user_id=query.from_user.id
    )
    await query.message.answer(
        text=text.success_change_notification, reply_markup=get_inline_menu()
    )


async def get_on_getting_notification(query: CallbackQuery) -> None:
    """Обработка on_getting_notification callback"""
    await db.change_user_notification(
        notification=text.on_getting_notification, user_id=query.from_user.id
    )
    await query.message.answer(
        text=text.success_change_notification, reply_markup=get_inline_menu()
    )


async def cancel_user_notification(query: CallbackQuery) -> None:
    """Обработка cancel_notification callback"""
    await db.delete_user_request(user_id=query.from_user.id)
    await query.message.answer(text=text.menu, reply_markup=get_inline_menu())


async def confirm_change_user_notification(query: CallbackQuery) -> None:
    """Обработка change_notification callback"""
    await query.message.answer(
        text=text.get_notification, reply_markup=notification_button()
    )


async def cancel_change_user_notification(query: CallbackQuery) -> None:
    """Обработка change_notification callback"""
    await query.message.answer(text=text.menu, reply_markup=get_inline_menu())
