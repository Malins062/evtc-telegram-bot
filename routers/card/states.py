from datetime import datetime
from typing import TypedDict, get_type_hints

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils import markdown

EMPTY = 'пусто'


class Card(TypedDict, total=False):
    dt: str
    gn: str
    model: str
    address: str
    article: str
    protocol: str


class CardStates(StatesGroup):
    dt = State()
    gn = State()
    model = State()
    address = State()
    article = State()
    protocol = State()


async def init_state(state: FSMContext) -> FSMContext:
    now_dt = datetime.now().strftime('%d.%m.%Y %H:%M')
    data: Card = {'dt': now_dt}
    new_state = state
    await new_state.clear()
    await new_state.update_data(data)
    return new_state


async def reset_state(state: FSMContext) -> FSMContext:
    current_state = await state.get_state()
    if current_state:
        await state.set_state(None)
    return state


def validate_card(data) -> bool:
    return all(data.get(key, False) for key in get_type_hints(Card))


def get_validate_symbol(is_valid: bool) -> str:
    return '✔' if is_valid else '❌'


def get_value_card_text(user_data, key):
    value = user_data.get(key, EMPTY)
    result = get_validate_symbol(value != EMPTY) + ' '
    result += f'{markdown.hitalic(value)}' if value == EMPTY else f'{markdown.hbold(value)}'
    return result


def get_card_text(user_data, user_id) -> str:
    text = markdown.text(
        markdown.hbold(f'🚔 КАРТОЧКА НАРУШЕНИЯ {get_validate_symbol(validate_card(user_data))} (#{user_id}) 🚔'),
        '',
        f'Дата и время: {get_value_card_text(user_data, "dt")}',
        f'Номер ТС: {get_value_card_text(user_data, "gn")}',
        f'Марка, модель: {get_value_card_text(user_data, "model")}',
        f'Адрес: {get_value_card_text(user_data, "address")}',
        f'Статья КоАП РФ: {get_value_card_text(user_data, "article")}',
        f'Протокол: {get_value_card_text(user_data, "protocol")}',
        '',
        sep='\n'
    )
    return text
