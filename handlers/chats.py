from aiogram import Bot, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from state import SendMessage
from logger import logger
from .rout import router
from db import db

from .texts import text

@router.callback_query(lambda c: c.data.startswith("send_twin:"))
async def send_twin_callback(
    query: types.CallbackQuery, state: FSMContext
):  # Add state
    """Обработчик callback-запроса для кнопки "Написать близнецу"."""
    language = db.get_user_language(query.from_user.id)
    try:
        twin_id = int(query.data.split(":")[1])  # Get twin_id from callback_data

        # Set state
        await state.update_data(recipient_id=twin_id)
        await state.set_state(SendMessage.message)
        # Save it to FSM
        await query.message.answer(text.send_message(language))  # Ask a message!
    except ValueError:
        await query.message.answer(text.send_error(language))
    except Exception as e:
        logger.exception(f"Ошибка при обработке callback send_twin: {e}")
        await query.message.answer(text.send_error_2(language))
    finally:
        await query.answer()  # Remove loading.


# Обработчик команды /send_message
@router.message(Command("send_message"))
async def send_message_command(message: types.Message, state: FSMContext):
    """Запускает процесс отправки сообщения другому пользователю."""
    language = db.get_user_language(message.from_user.id)
    await state.set_state(SendMessage.telegram_id)
    await message.reply(
        text.set_id(language)
    )


# Обработчик состояния SendMessage.telegram_id
@router.message(SendMessage.telegram_id, F.text)
async def telegram_id_entered_handler(message: types.Message, state: FSMContext):
    """Получает telegram_id получателя и переходит к запросу сообщения."""
    language = db.get_user_language(message.from_user.id)
    try:

        recipient_id = int(message.text)
        await state.update_data(recipient_id=recipient_id)
        await state.set_state(SendMessage.message)
        await message.reply(text.send_message(language))#
    except ValueError:
        await message.reply(text.send_error(language))
    except Exception as e:
        logger.exception(f"Ошибка при получении telegram_id: {e}")
        await message.reply(text.send_error_2(language))


# Обработчик состояния SendMessage.message
@router.message(SendMessage.message, F.text)
async def message_entered_handler(message: types.Message, state: FSMContext, bot: Bot):
    """Получает сообщение и отправляет его выбранному пользователю."""
    language = db.get_user_language(message.from_user.id)
    try:
        data = await state.get_data()
        recipient_id = data.get("recipient_id")
        message_text = message.text

        if message_text == "/cancel":
            await state.clear()
            await message.reply("Отменено.", reply_markup=types.ReplyKeyboardRemove())  # optional: Reply to user
            return  # Прерываем выполнение функции

        db.send_message(
            message=message_text,
            recipient_id=recipient_id,
            telegram_id=message.from_user.id,
        )
        await bot.send_message(
            recipient_id,
            f"{message.from_user.first_name} (ID: {message.from_user.id}):\n{message_text}",
        )
        await message.reply(text.message_success(language))
    except Exception as e:
        logger.exception(f"Ошибка при отправке сообщения: {e}")
        await message.reply(text.send_error_2(language))
    finally:
        await state.set_state(SendMessage.message)
