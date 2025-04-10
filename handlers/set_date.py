from aiogram import Bot, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from state import NameDate
from .rout import router

from .texts import text
from db import db


@router.message(Command("set_date_and_name"))
async def set_date_and_name_command(message: types.Message, state: FSMContext):
    """Запускает процесс установки имени и даты рождения."""
    if message.text == "/cancel":
        await state.clear()
        await message.reply("Отменено.", reply_markup=types.ReplyKeyboardRemove())  # optional: Reply to user
        return  # Прерываем выполнение функции
    await state.set_state(NameDate.name)
    lang = db.get_user_language(message.from_user.id)
    await message.reply(text.enter_name(lang))


# Обработчик состояния NameDate.name
@router.message(NameDate.name, F.text)
async def name_entered_handler(message: types.Message, state: FSMContext):
    """Получает имя пользователя и переходит к запросу даты рождения."""
    if message.text == "/cancel":
        await state.clear()
        await message.reply("Отменено.", reply_markup=types.ReplyKeyboardRemove())  # optional: Reply to user
        return  # Прерываем выполнение функции
    await state.update_data(name=message.text)
    await state.set_state(NameDate.date)
    lang = db.get_user_language(message.from_user.id)
    await message.reply(text.enter_date(lang))


@router.message(NameDate.date)
async def name_entered(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id
    db.set_name_and_date(
        telegram_id=telegram_id, name=data["name"], date_of_bird=data["date"]
    )
    await state.clear()
    keyboard = InlineKeyboardBuilder()
    lang = db.get_user_language(message.from_user.id)
    keyboard.button(text=text.find_twin(lang), callback_data="find_twin")

    # 2. Отправляем сообщение с клавиатурой
    await message.reply(text.name_entered(lang)
        ,
        reply_markup=keyboard.as_markup(),
    )
