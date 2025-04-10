from aiogram.fsm.state import State, StatesGroup


class NameDate(StatesGroup):
    language = State()
    name = State()
    date = State()


class SendMessage(StatesGroup):
    telegram_id = State()
    message = State()
    recipient_id = State()


class Post(StatesGroup):
    text = State()
