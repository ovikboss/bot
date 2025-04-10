from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter

from .rout import router  # Импортируем router из rout.py
from state import NameDate  # Assuming you have a state.py with NameDate


@router.message(Command("cancel"), StateFilter("*"))
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Отменяет текущее состояние (FSM) и возвращает пользователя в начальное состояние.
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.reply(
            "Нечего отменять.", reply_markup=types.ReplyKeyboardRemove()
        )
        return

    print(f"Отмена состояния {current_state!r}")
    await state.clear()
    await message.reply("Отменено.", reply_markup=types.ReplyKeyboardRemove())