from _apps.individual_tg_bot import text
from _apps.individual_tg_bot.service import show_summary
from _apps.individual_tg_bot.settings import APP_HOST, APP_PORT
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from urllib.parse import quote



async def key_word_handler(
    message: Message,
    state: FSMContext,
) -> None:
    """Обработка ключевого слова"""

    await state.update_data(keyword=message.text)
    data = await state.get_data()
    base_url = f"http://{APP_HOST}:{APP_PORT}/user_requests_vacancies"
    link = (
        base_url
        + "?"
        + quote("&".join([f"{key}={value}" for key, value in data.items()]))
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Перейти к вакансиям", url=link))
    await message.answer(text=text.thanks_text, reply_markup=keyboard)
    data["selected_notification"] = text.on_getting_notification
    await show_summary(message=message, data=data)

    await state.finish()
