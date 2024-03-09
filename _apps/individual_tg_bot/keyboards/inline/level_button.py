from _apps.individual_tg_bot import text
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

level_button_dict = {
    text.junior: text.junior,
    text.middle: text.middle,
    text.senior: text.senior,
    text.tech_lead: text.tech_lead,
    text.accept_level: text.accept_level,
}


def level_button():
    """Уровень владения профессией"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in level_button_dict.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard
