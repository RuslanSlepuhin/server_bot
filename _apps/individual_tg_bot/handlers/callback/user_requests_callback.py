from _apps.individual_tg_bot.handlers.callback.callback_service import (
    user_request_filter,
)
from _apps.individual_tg_bot.keyboards.inline.direction_buton import (
    get_direction_button,
)
from _apps.individual_tg_bot.keyboards.inline.main_menu import get_inline_menu
from _apps.individual_tg_bot.service import db
from aiogram.types import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from _apps.individual_tg_bot import text


async def filter_history_callback(query: CallbackQuery) -> None:
    result = await db.get_user_request(user_id=query.from_user.id)
    keyboard = InlineKeyboardMarkup()
    for request in result:
        button_text = "/".join(
            [
                request.get("direction", ""),
                request.get("specialization", ""),
                request.get("level", ""),
            ]
        )
        callback_data = f'request_{request["id"]}'
        keyboard.add(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    keyboard.add(
        InlineKeyboardButton(text=text.back_to_menu, callback_data=text.back_to_menu)
    )
    await query.message.answer(
        text="Ваши запросы:",
        reply_markup=keyboard,
    )


async def process_request_callback(query: CallbackQuery):
    request_id = query.data.split("_")[1]
    result = await db.get_user_filter(record_id=int(request_id))
    data = await user_request_filter(data=result)
    await query.message.answer(text=f"{data}")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text.change, callback_data=f"{text.change}_{request_id}"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=text.delete, callback_data=f"{text.delete}_{request_id}"
        )
    )
    keyboard.add(
        InlineKeyboardButton(text=text.back_to_menu, callback_data=text.back_to_menu)
    )
    await query.message.answer(text="Дальнейшие действия: ", reply_markup=keyboard)


async def delete_user_filter(query: CallbackQuery) -> None:
    """Обработка удаления запроса от пользователя"""
    request_id = query.data.split("_")[1]
    await db.delete_user_request(record_id=int(request_id))
    await query.message.answer(text=text.menu, reply_markup=get_inline_menu())


async def change_user_filter(query: CallbackQuery) -> None:
    """Обработка изменения запроса от пользователя"""
    request_id = query.data.split("_")[1]
    await db.delete_user_request(record_id=int(request_id))
    await query.message.answer(text=text.direction, reply_markup=get_direction_button())
