from aiogram import Bot, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from state import Post
from logger import logger
from .rout import router


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
