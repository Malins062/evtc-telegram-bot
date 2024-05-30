from aiogram.fsm.state import StatesGroup, State

EMPTY = 'пусто'


class Card(StatesGroup):
    gn = State()
    model = State()
    address = State()
    article = State()
    protocol = State()
    validated = State()
