from _apps.individual_tg_bot import text

from _apps.individual_tg_bot.keyboards.inline.notifications import (
    notification_survey_button,
)

from aiogram.dispatcher import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
)


async def key_word_handler_text(
    query: CallbackQuery,
) -> None:
    """Обработка кнопки ответить текстом"""
    await query.message.answer(
        text="Введите ключевые слова: ",
        reply_markup=ReplyKeyboardRemove(),
    )


async def key_word_handler(
    message: Message,
    state: FSMContext,
) -> None:
    """Обработка ключевого слова"""
    await state.update_data(keyword=message.text)
    data = await state.get_data()

    selected_key_word = data.get("keyword", set())
    await message.answer(
        text=f"{text.chosen_keyword} {selected_key_word}\n{text.get_notification}",
        reply_markup=notification_survey_button(),

    )
    return


async def key_word_handler_skip(query: CallbackQuery, state: FSMContext):
    """Обработка кнопки Пропустить"""
    await state.update_data(keyword="")
    await query.message.answer(
        text=f"{text.chosen_keyword}\n{text.get_notification}",
        reply_markup=notification_survey_button(),
    )
    return
