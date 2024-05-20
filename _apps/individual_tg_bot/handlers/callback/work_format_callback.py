from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.handlers.callback.callback_service import (
    confirm_choice_handler,
)
from _apps.individual_tg_bot.keyboards.inline.work_format import work_format_dict
from aiogram.dispatcher import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


async def work_format_callback_handler(query: CallbackQuery, state: FSMContext) -> None:
    """Обработка callback для формата работы"""
    data = await state.get_data()

    selected_work_format = data.get("selected_work_format", set())

    keyboard_skip = InlineKeyboardMarkup()
    keyboard_skip.add(
        InlineKeyboardButton(text=text.skip_add_info, callback_data=text.skip_add_info)
    )
    keyboard_skip.add(
        InlineKeyboardButton(text=text.add_info_text, callback_data=text.add_info_text)
    )

    if text.accept_format in query.data:
        await query.message.answer(
            text=f"{text.chosen_format} {', '.join(selected_work_format)}\n{text.add_info}\n{text.add_info_additional}",
            reply_markup=keyboard_skip,
        )
        return

    if query.data in work_format_dict:
        await confirm_choice_handler(
            query=query,
            selected_specializations=selected_work_format,
            buttons_dict=work_format_dict,
        )

    await state.update_data(selected_work_format=selected_work_format)
