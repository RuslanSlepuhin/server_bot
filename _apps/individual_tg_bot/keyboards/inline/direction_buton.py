from _apps.individual_tg_bot import text
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def get_direction_button():
    """Inline клавиатура для направления меню"""
    inline_keyboard = InlineKeyboardMarkup(row_width=5)
    inline_keyboard.add(
        InlineKeyboardButton(text=text.design, callback_data=text.design)
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.backend, callback_data=text.backend)
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.analyst, callback_data=text.analyst)
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.mobile, callback_data=text.mobile)
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.marketing, callback_data=text.marketing)
    )
    inline_keyboard.add(
        InlineKeyboardButton(
            text=text.product_project_manager,
            callback_data=text.product_project_manager,
        )
    )
    inline_keyboard.add(InlineKeyboardButton(text=text.sales, callback_data=text.sales))
    inline_keyboard.add(
        InlineKeyboardButton(text=text.dev_ops, callback_data=text.dev_ops)
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.frontend, callback_data=text.frontend)
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.support, callback_data=text.support)
    )
    inline_keyboard.add(
        InlineKeyboardButton(text=text.fullstack, callback_data=text.fullstack)
    )
    inline_keyboard.add(InlineKeyboardButton(text=text.hr, callback_data=text.hr))
    inline_keyboard.add(
        InlineKeyboardButton(text=text.game_dev, callback_data=text.game_dev)
    )
    inline_keyboard.add(InlineKeyboardButton(text=text.qa, callback_data=text.qa))
    return inline_keyboard
