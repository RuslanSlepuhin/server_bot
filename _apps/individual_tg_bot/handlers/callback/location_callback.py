from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.handlers.callback.callback_service import (
    confirm_choice_handler,
)
from _apps.individual_tg_bot.keyboards.inline.location_button import (
    location_button_dict,
)
from _apps.individual_tg_bot.keyboards.inline.work_format import work_format_button
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery


async def location_callback_handler(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback для локации"""
    data = await state.get_data()
    selected_location = data.get("selected_location", set())

    if text.accept_location in query.data:
        await query.message.answer(
            text=f"{text.chosen_location} {', '.join(selected_location)}\n{text.work_format}\n{text.multiple_choice}",
            reply_markup=work_format_button(),
        )
        return

    if query.data in location_button_dict:
        await confirm_choice_handler(
            query=query,
            selected_specializations=selected_location,
            buttons_dict=location_button_dict,
        )

    await state.update_data(selected_location=selected_location)
