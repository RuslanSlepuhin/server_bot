from typing import Dict

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


async def confirm_choice_handler(
    query: CallbackQuery, selected_specializations: set, buttons_dict: dict
):
    if query.data in selected_specializations:
        selected_specializations.remove(query.data)
        button_text_prefix = "❌"
    else:
        selected_specializations.add(query.data)
        button_text_prefix = "✅"

    updated_keyboard = InlineKeyboardMarkup()
    for button_text, button_callback in buttons_dict.items():
        button_text_with_prefix = (
            f"{button_text_prefix} {button_text}"
            if button_callback in selected_specializations
            else button_text
        )
        updated_keyboard.add(
            InlineKeyboardButton(
                text=button_text_with_prefix, callback_data=button_callback
            )
        )

    await query.message.edit_reply_markup(
        reply_markup=updated_keyboard,
    )


async def user_digest(data: Dict) -> str:
    res_str = (
        f"Выбранное направление: {data.get('selected_direction', '')}\n"
        f"Выбранная специализация: {', '.join(data.get('selected_specializations', ''))}\n"
    )
    return res_str


async def user_request_filter(data: Dict) -> str:
    res_str = (
        f"Выбранное направление: {data.get('direction', '')}\n"
        f"Выбранная специализация: {(data.get('specialization', ''))}\n"
        f"Выбранный уровень: {(data.get('level', ''))}\n"
        f"Выбранная локация: {(data.get('location', ''))}\n"
        f"Выбранный формат работы: {(data.get('work_format', ''))}\n"
        f"Ключевое слово: {data.get('keywords', '')}\n"
        f"Периодичность уведомлений: {data.get('selected_notification', '')[2:-2]}\n"
    )
    return res_str
