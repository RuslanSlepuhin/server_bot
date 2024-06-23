from _apps.individual_tg_bot.handlers.callback.callback_service import (
    user_request_filter,
)
from _apps.individual_tg_bot.keyboards.inline.direction_buton import (
    get_direction_button,
)
from _apps.individual_tg_bot.keyboards.inline.main_menu import get_inline_menu
from aiogram.types import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.service import get_user_request, send_delete_request
from _apps.itcoty_web.itcoty_web.settings import URL_USER_REQUEST


async def filter_history_callback(query: CallbackQuery) -> None:

    keyboard = InlineKeyboardMarkup()
    result_all = await get_user_request(user_id=query.from_user.id)
    if result_all:
        for result in result_all.get('results'):
            button_text = "/".join(
                [
                    result.get("direction", ""),
                    result.get("specialization", ""),
                    result.get("level", ""),
                ]
            )
            callback_data = f'request_{result["id"]}'
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
    record_id = query.data.split("_")[1]
    result = await get_user_request(data_id=record_id)
    data = await user_request_filter(data=result.get('results')[0])
    await query.message.answer(text=f"{data}")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text.change, callback_data=f"{text.change}_{record_id}"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=text.delete, callback_data=f"{text.delete}_{record_id}"
        )
    )
    keyboard.add(
        InlineKeyboardButton(text=text.back_to_menu, callback_data=text.back_to_menu)
    )
    await query.message.answer(text="Дальнейшие действия: ", reply_markup=keyboard)


async def delete_user_filter(query: CallbackQuery) -> None:
    """Обработка удаления запроса от пользователя"""
    request_id = query.data.split("_")[1]
    url = URL_USER_REQUEST + f'{request_id}/'
    await send_delete_request(url=url)
    await query.message.answer(text=text.menu, reply_markup=get_inline_menu())


async def change_user_filter(query: CallbackQuery) -> None:
    """Обработка изменения запроса от пользователя"""
    request_id = query.data.split("_")[1]
    url = URL_USER_REQUEST + f'{request_id}/'
    await send_delete_request(url=url)
    await query.message.answer(text=text.direction, reply_markup=get_direction_button())
