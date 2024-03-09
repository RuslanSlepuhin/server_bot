from _apps.individual_tg_bot import text
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

location_button_dict = {
    text.russia: text.russia,
    text.belarus: text.belarus,
    text.europe: text.europe,
    text.other_location: text.other_location,
    text.accept_location: text.accept_location,
}


def location_button():
    """Уровень владения профессией"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in location_button_dict.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard
