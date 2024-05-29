from aiogram import types


async def set_default_commands(bot):
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Запустить бота"),
            types.BotCommand(command="count_today_vacancies", description="Вакансий в сутки в разрезе ресурсов"),
            types.BotCommand(command="help", description="Другие команды"),
        ]
    )
