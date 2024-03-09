from _apps.individual_tg_bot import text
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

work_format_dict = {
    text.remote: text.remote,
    text.office: text.office,
    text.hybrid: text.hybrid,
    text.any_format: text.any_format,
    text.accept_format: text.accept_format,
}


def work_format_button():
    """Inline клавиатура для формата работы"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in work_format_dict.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard
