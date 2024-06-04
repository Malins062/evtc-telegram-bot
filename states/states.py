from typing import TypedDict, get_type_hints

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils import markdown

from config_data.config import input_data
from utils.common import get_now

EMPTY = 'пусто'


class Card(TypedDict, total=False):
    dt: str
    gn: str
    model: str
    address: str
    article: str
    protocol: str
    parking: str
    user_id: int


class CardStates(StatesGroup):
    dt = State()
    article = State()
    gn = State()
    model = State()
    address = State()
    protocol = State()
    parking = State()


def set_input_data(state: FSMContext, data: Card) -> Card:
    user_id = state.key.user_id
    if user_id not in input_data:
        input_data[user_id] = data
    else:
        input_data[user_id].update(data)
    return input_data[user_id]


async def init_state(state: FSMContext) -> FSMContext:
    user_id = state.key.user_id
    input_data.pop(user_id , None)
    set_input_data(state, Card(dt=get_now(), user_id=user_id))
    new_state = state
    await new_state.clear()
    return new_state


async def reset_state(state: FSMContext) -> FSMContext:
    current_state = await state.get_state()
    if current_state:
        await state.set_state(None)
    return state


def validate_card(data) -> bool:
    if data:
        return all(data.get(key, False) for key in get_type_hints(Card))
    else:
        return False


def get_validate_symbol(is_valid: bool) -> str:
    return '✔' if is_valid else '❌'


def get_value_card_text(user_data, key):
    value = user_data.get(key, EMPTY) if user_data else EMPTY
    result = get_validate_symbol(value != EMPTY) + ' '
    result += f'{markdown.hitalic(value)}' if value == EMPTY else f'{markdown.hbold(value)}'
    return result


def get_card_text(user_data, user_id) -> str:
    text = markdown.text(
        markdown.hbold(f'🚔 КАРТОЧКА НАРУШЕНИЯ {get_validate_symbol(validate_card(user_data))}'),
        markdown.hbold(f'(👮‍♂️ - {user_id})'),
        '',
        f'Дата и время: {get_value_card_text(user_data, "dt")}',
        f'Номер ТС: {get_value_card_text(user_data, "gn")}',
        f'Марка, модель: {get_value_card_text(user_data, "model")}',
        f'Адрес: {get_value_card_text(user_data, "address")}',
        f'Статья КоАП РФ: {get_value_card_text(user_data, "article")}',
        f'Протокол: {get_value_card_text(user_data, "protocol")}',
        f'Стоянка: {get_value_card_text(user_data, "parking")}',
        '',
        sep='\n'
    )
    return text
