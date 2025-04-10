from aiogram import Bot, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from logger import logger
from .rout import router
from db import db
from .texts import text


async def find_and_reply_twins(
    message: types.Message, user_id: int, bot: Bot
):  # Added Bot argument
    """Выполняет поиск и отправляет ответ о близнецах."""
    language = db.get_user_language(user_id)
    try:
        users = db.find_user(user_id)
        keyboard = InlineKeyboardBuilder()
        await bot.send_message(
                    message.chat.id,
                    f"Найдено {len(users)} близнецов")
        if users:
            for user in users:
                keyboard = InlineKeyboardBuilder()  # Create for each user.

                keyboard.button(
                    text=text.send_twin(language),
                    callback_data=f"send_twin:{user.telegram_id}",
                )
                await bot.send_message(
                    message.chat.id,
                    f"{text.twin_find(language)}: {user.name} (Telegram ID: {user.telegram_id})\n {text.send_button(language)}",
                    reply_markup=keyboard.as_markup(),
                )

        else:

            await bot.send_message(
                message.chat.id,
                text.not_twins(language),
            )
    except Exception as e:
        logger.exception(f"Ошибка при поиске близнецов: {e}")
        await bot.send_message(
            message.chat.id, text.find_twin_error(language)
        )


# Обработчик команды /find_twin
@router.message(Command("find_twin"))
async def find_twin_command(message: types.Message, bot: Bot):
    """Находит астрологических близнецов пользователя."""
    await find_and_reply_twins(message, message.from_user.id, bot)


@router.callback_query(F.data == "find_twin")
async def find_twin_callback(query: types.CallbackQuery, bot: Bot):  # Add bot argument.
    """Обработчик callback-запроса для кнопки "Найти близнеца"."""
    # Вызов общего кода
    await find_and_reply_twins(query.message, query.from_user.id, bot)  # Pass bot.
    # It does not need special keyboard creation!
