import asyncio
from aiogram import Bot, types, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.rout import router

storage = MemoryStorage()

dp = Dispatcher(storage=storage)


TOKEN = "7937455538:AAGoggXJEyNvtsVX8pyBY-dnSuEpXnz86ZY"

bot = Bot(token=TOKEN)


async def set_commands(bot: Bot):
    """Устанавливает команды для меню бота."""
    commands = [
        types.BotCommand(command="start", description="Начать работу с ботом"),
        types.BotCommand(command="help", description="Помощь по командам бота"),
        types.BotCommand(
            command="find_twin", description="Найти астрологического близнеца"
        ),
        types.BotCommand(command="send_message", description="Отправить сообщение"),
        types.BotCommand(
            command="set_date_and_name", description="Установить имя и дату рождения"
        ),
        types.BotCommand(command="cancel", description="Выйти из режима чата"),
        types.BotCommand(command="language", description="Сменить язык"),
    ]
    await bot.set_my_commands(commands)


async def main():

    await set_commands(bot)

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
