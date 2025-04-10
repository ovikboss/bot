from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from state import NameDate
from .rout import router

from .set_language import language_keyboard_2
from logger import logger
from db import db





@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    """Приветствует пользователя и создает его в базе данных."""
    try:
        db.create_user(telegram_id=message.from_user.id)
        await message.reply(
            """ Привет! Это бот для поиска человека, рождённого с вами в один день и год! 
        Вы можете общаться прямо в боте или перейти в личные сообщения. 
        Канал - @mukunda_centr
        Контакты - @Maria_Prokhorova"""
        )
        await message.reply(
            "Пожалуйста, выберите язык:", reply_markup=language_keyboard_2
        )
        await state.set_state(NameDate.language)  # NEW LINE. SET STATE TO LANGUAGE
    except Exception as e:
        logger.exception(f"Ошибка при создании пользователя: {e}")
        await message.reply("Произошла ошибка при создании пользователя.")


@router.message(Command("help"))
async def help_command(message: types.Message):
    """Предоставляет информацию о доступных командах."""
    await message.reply(
        "Вот список доступных команд:\n"
        "/start - Начать работу с ботом\n"
        "/set_date_and_name - Установить имя и дату рождения\n"
        "/find_twin - Найти астрологического близнеца\n"
        "/send_message - Отправить сообщение другому пользователю\n"
    )
