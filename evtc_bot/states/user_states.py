from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    get_phone = State()
    add_phone = State()
    remove_phone = State()
