from aiogram.fsm.state import StatesGroup, State


class Card(StatesGroup):
    gn = State()
    protocol = State()
    address = State()
    article = State()
    validated = State()
