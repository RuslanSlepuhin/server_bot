from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.keyboards.inline.level_button import level_button
from _apps.individual_tg_bot.keyboards.inline.specializations.buttons import (
    buttons_dev_ops,
)
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


async def dev_ops_specialization_callback(
    query: CallbackQuery, state: FSMContext
) -> None:
    """Обработка callback для dev_ops направления"""
    data = await state.get_data()

    selected_specializations = data.get("selected_specializations", set())

    if text.accept in query.data:
        await query.message.answer(
            text=f"{text.chosen_specialization} {', '.join(selected_specializations)}\n{text.level}",
            reply_markup=level_button(),
        )
        return

    if query.data in buttons_dev_ops:
        selected_specializations.add(query.data)

    await state.update_data(selected_specializations=selected_specializations)

    updated_keyboard = InlineKeyboardMarkup()
    for button_text, button_callback in buttons_dev_ops.items():
        if button_callback not in selected_specializations:
            updated_keyboard.add(
                InlineKeyboardButton(text=button_text, callback_data=button_callback)
            )

    if query.data in selected_specializations:
        await query.message.answer(
            text=f"{text.chosen_specialization} {', '.join(selected_specializations)}",
            reply_markup=updated_keyboard,
        )
        return
