from _apps.individual_tg_bot import text
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

notification_dict = {
    text.per_day_notification: text.per_day_notification,
    text.on_getting_notification: text.on_getting_notification,
    text.cancel_notification: text.cancel_notification,
}

change_notification_dict = {
    text.confirm_change_notification: text.confirm_change_notification,
    text.cancel_change_notification: text.cancel_change_notification,
}


def notification_button():
    """Клавиатура для уведомлений"""

    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    for button_text, button_callback in notification_dict.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def change_notification():
    """Смена выбранного уведомления"""

    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    for button_text, button_callback in change_notification_dict.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard
