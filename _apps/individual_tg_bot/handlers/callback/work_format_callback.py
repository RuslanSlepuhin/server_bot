from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.keyboards.inline.work_format import work_format_dict
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)


async def work_format_callback_handler(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback для формата работы"""
    data = await state.get_data()

    selected_work_format = data.get("selected_work_format", set())

    if text.accept_format in query.data:
        await query.message.answer(
            text=f"{text.chosen_format} {', '.join(selected_work_format)}\n{text.add_info}",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    if query.data in work_format_dict:
        selected_work_format.add(query.data)

    await state.update_data(selected_work_format=selected_work_format)

    updated_keyboard = InlineKeyboardMarkup()
    for button_text, button_callback in work_format_dict.items():
        if button_callback not in selected_work_format:
            updated_keyboard.add(
                InlineKeyboardButton(text=button_text, callback_data=button_callback)
            )

    if query.data in selected_work_format:
        await query.message.answer(
            text=f"{text.chosen_format} {', '.join(selected_work_format)}",
            reply_markup=updated_keyboard,
        )
        return
