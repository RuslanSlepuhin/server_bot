from _apps.individual_tg_bot.text import come_back, reset_request
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

new_request_button_dict = {reset_request: reset_request, come_back: come_back}


def new_request_button():
    """Уровень владения профессией"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in new_request_button_dict.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard
