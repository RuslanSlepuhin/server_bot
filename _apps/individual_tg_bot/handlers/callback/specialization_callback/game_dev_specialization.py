from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.handlers.callback.callback_service import (
    confirm_choice_handler,
)
from _apps.individual_tg_bot.keyboards.inline.level_button import level_button
from _apps.individual_tg_bot.keyboards.inline.specializations.buttons import (
    buttons_game_dev,
)
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery


async def game_dev_specialization_callback(
    query: CallbackQuery, state: FSMContext
) -> None:
    """Обработка callback для game_dev направления"""
    data = await state.get_data()

    selected_specializations = data.get("selected_specializations", set())

    if text.accept in query.data:
        await query.message.answer(
            text=f"{text.chosen_specialization} {', '.join(selected_specializations)}\n{text.level}\n{text.multiple_choice}",
            reply_markup=level_button(),
        )
        return

    if query.data in buttons_game_dev:
        await confirm_choice_handler(
            query=query,
            selected_specializations=selected_specializations,
            buttons_dict=buttons_game_dev,
        )

    await state.update_data(selected_specializations=selected_specializations)
