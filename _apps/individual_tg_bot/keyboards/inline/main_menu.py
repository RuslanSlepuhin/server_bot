from _apps.individual_tg_bot import text
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_menu():
    """Inline клавиатура для главного меню"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    inline_keyboard.add(
        InlineKeyboardButton(
            text=text.vacancy_filter, callback_data=text.vacancy_filter
        )
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.notification, callback_data=text.notification)
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.user_profile, url="https://itcoty.ru/")
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.restart, callback_data=text.restart)
    )
    return inline_keyboard
