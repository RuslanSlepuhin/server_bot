from aiogram import types

from _apps.ask_gpt.bot.variables import chat_gpt_sales_manager, chat_gpt_without_history


async def set_default_commands(bot):
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Запустить бота"),
            types.BotCommand(command=chat_gpt_sales_manager, description="Сэйл в Simpleatom (история суммарно 10 последних сообщений + промпт)"),
            types.BotCommand(command=chat_gpt_without_history, description="Ответ на вопрос без сохранении истории"),
        ]
    )