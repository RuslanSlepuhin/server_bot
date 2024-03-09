from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.keyboards.inline.main_menu import get_inline_menu
from _apps.individual_tg_bot.keyboards.inline.notifications import notification_button
from _apps.individual_tg_bot.service import db
from aiogram.types import CallbackQuery


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
