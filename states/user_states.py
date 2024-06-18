from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    get_phone = State()
    add_phone = State()
    remove_phone = State()
