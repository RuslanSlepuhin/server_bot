from _apps.individual_tg_bot.keyboards.inline.specializations.buttons import (
    buttons_analyst,
    buttons_backend,
    buttons_design,
    buttons_dev_ops,
    buttons_frontend,
    buttons_fullstack,
    buttons_game_dev,
    buttons_hr,
    buttons_marketing,
    buttons_mobile,
    buttons_product_project_manager,
    buttons_qa,
    buttons_sales,
    buttons_support,
)
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def design_button():
    """Кнопки специализации Design"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_design.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def backend_button():
    """Кнопки специализации backend"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_backend.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def analyst_button():
    """Кнопки специализации analyst"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_analyst.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def mobile_button():
    """Кнопки специализации mobile"""
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    for button_text, button_callback in buttons_mobile.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def marketing_button():
    """Кнопки специализации marketing"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_marketing.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def product_project_manager_button():
    """Кнопки специализации Product & Project manager"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_product_project_manager.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def sales_button():
    """Кнопки специализации Sales"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_sales.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def dev_ops_button():
    """Кнопки специализации DevOps"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_dev_ops.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def frontend_button():
    """Кнопки специализации Frontend"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_frontend.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def support_button():
    """Кнопки специализации Support"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_support.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def fullstack_button():
    """Кнопки специализации Fullstack"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_fullstack.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def hr_button():
    """Кнопки специализации HR"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_hr.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def game_dev_button():
    """Кнопки специализации GameDev"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_game_dev.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard


def qa_button():
    """Кнопки специализации QA"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    for button_text, button_callback in buttons_qa.items():
        inline_keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=button_callback)
        )
    return inline_keyboard
