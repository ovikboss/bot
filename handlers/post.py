from aiogram import Bot, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from state import Post
from logger import logger
from .rout import router
from db import db
from aiogram.exceptions import TelegramForbiddenError
from aiogram.enums import ParseMode # Import ParseMode


@router.message(Command("post"))
async def message_entered_handler(message: types.Message, state: FSMContext):
    try:
        if message.from_user.id == 229258201:
            await state.set_state(Post.text)
            await message.reply("Введите текст для поста")
        else:
            await message.reply("Нет прав")
    except Exception as e:
        logger.exception(f"Ошибка при отправке сообщения: {e}")
        await message.reply("Произошла ошибка при отправке сообщения.")

@router.message(Post.text, F.text)
async def post_text_entered(message: types.Message, state: FSMContext, bot: Bot):
    """После ввода текста поста - рассылка."""
    try:
        post_text = message.text
        # 1. Получаем список всех пользователей
        users = db.get_users()  # You need to implement this function in db.py

        # 2. Рассылка сообщения
        if users:
            for user in users:
                try:
                    await bot.send_message(
                        user,
                        post_text,
                        parse_mode=ParseMode.HTML, # for HTML formatting
                    )
                    logger.info(f"Сообщение отправлено пользователю {user.telegram_id}")
                except TelegramForbiddenError:
                    logger.warning(f"Пользователь {user.telegram_id} заблокировал бота.")
                except Exception as e:
                    logger.error(
                        f"Ошибка при отправке сообщения пользователю {user.telegram_id}: {e}"
                    )
        else:
            await message.reply("Нет пользователей для рассылки.")

        await message.reply("Рассылка завершена.")  # Отправляем подтверждение
    except Exception as e:
        logger.exception(f"Ошибка при рассылке: {e}")
        await message.reply("Произошла ошибка при рассылке.")
    finally:
        await state.clear()  # Очищаем состояние FSM