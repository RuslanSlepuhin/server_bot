from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.keyboards.inline.level_button import level_button_dict
from _apps.individual_tg_bot.keyboards.inline.location_button import location_button
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


async def level_callback_handler(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback для уровня владения"""
    data = await state.get_data()
    selected_level = data.get("selected_level", set())

    if text.accept_level in query.data:
        await query.message.answer(
            text=f"{text.chosen_level} {', '.join(selected_level)}\n{text.location}",
            reply_markup=location_button(),
        )
        return

    if query.data in level_button_dict:
        selected_level.add(query.data)

    await state.update_data(selected_level=selected_level)

    updated_keyboard = InlineKeyboardMarkup()
    for button_text, button_callback in level_button_dict.items():
        if button_callback not in selected_level:
            updated_keyboard.add(
                InlineKeyboardButton(text=button_text, callback_data=button_callback)
            )

    if query.data in selected_level:
        await query.message.answer(
            text=f"{text.chosen_level} {', '.join(selected_level)}",
            reply_markup=updated_keyboard,
        )
        return
