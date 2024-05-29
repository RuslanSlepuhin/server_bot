from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.handlers.callback.callback_service import (
    confirm_choice_handler,
)
from _apps.individual_tg_bot.keyboards.inline.level_button import level_button_dict
from _apps.individual_tg_bot.keyboards.inline.location_button import location_button
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery


async def level_callback_handler(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback для уровня владения"""
    data = await state.get_data()
    selected_level = data.get("selected_level", set())

    if text.accept_level in query.data:
        await query.message.answer(
            text=f"{text.chosen_level} {', '.join(selected_level)}\n{text.location}\n{text.multiple_choice}",
            reply_markup=location_button(),
        )
        return

    if query.data in level_button_dict:
        await confirm_choice_handler(
            query=query,
            selected_specializations=selected_level,
            buttons_dict=level_button_dict,
        )
    await state.update_data(selected_level=selected_level)
