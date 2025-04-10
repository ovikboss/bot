from aiogram import Bot, types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.enums import ParseMode

from state import NameDate
from logger import logger
from db import db

from .rout import router


# Create inline keyboard for language selection
language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang:en"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        ]
    ]
)

language_keyboard_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="Lang:en"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="Lang:ru"),
        ]
    ]
)


@router.message(Command("language"))
async def language_command(message: types.Message):
    await message.reply(text = "select language" , reply_markup = language_keyboard)

@router.callback_query(lambda c: c.data.startswith("lang:en"))
async def set_en(query: types.CallbackQuery):
    language_code = query.data.split(":")[1]
    db.set_user_language(
        telegram_id=query.from_user.id, language_code=language_code
    )  # Сохраняем язык!



@router.callback_query(lambda c: c.data.startswith("lang:ru"))
async def set_ru(query: types.CallbackQuery):
    language_code = query.data.split(":")[1]
    db.set_user_language(
        telegram_id=query.from_user.id, language_code=language_code
    )  # Сохраняем язык!



@router.callback_query(NameDate.language, lambda c: c.data.startswith("Lang:"))
async def language_callback(query: types.CallbackQuery, state: FSMContext):
    """Handles language selection callback."""
    try:
        language_code = query.data.split(":")[1]
        # Validate the language code.

        db.set_user_language(
            telegram_id=query.from_user.id, language_code=language_code
        )  # Сохраняем язык!
        await state.update_data(language=language_code)  # Сохраняем язык в FSM
        if language_code == "ru":
            await query.message.edit_text(
                f"Вы выбрали {language_code} язык!\nДавайте найдём вашего астро-близнеца! Напишите, пожалуйста, ваше имя",
                reply_markup=None,
            )  # Выводим язык
        else:
            await query.message.edit_text(
                f"You have selected {language_code} language!\nLet’s find your astro-twin! Please, enter your name",
                reply_markup=None,
            )  # Выводим язык
        await state.set_state(NameDate.name)  # Переходим к запросу имени

    except Exception as e:
        logger.exception(f"Ошибка при выборе языка: {e}")
        await query.message.answer("Произошла ошибка при выборе языка.")
    finally:
        await query.answer()  # To remove the loading.
