from typing import TypedDict, get_type_hints

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils import markdown

from config_data.admin import get_phones
from config_data.config import input_data, users
from utils.bot_files import delete_files_startswith
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
    photo_protocol: str
    photo_tc: str
    phone_number: str
    user_id: int


class CardStates(StatesGroup):
    dt = State()
    article = State()
    gn = State()
    model = State()
    address = State()
    protocol = State()
    parking = State()
    photo_protocol = State()
    photo_tc = State()


class PhotoStates(StatesGroup):
    tc = CardStates.photo_tc
    protocol = CardStates.photo_protocol


def set_input_data(state: FSMContext, data: Card) -> Card:
    user_id = state.key.user_id
    if user_id not in input_data:
        input_data[user_id] = data
    else:
        input_data[user_id].update(data)

    return input_data[user_id]


async def init_state(state: FSMContext) -> FSMContext:
    user_id = state.key.user_id

    # Access verification
    user_phone_number = users.get(user_id)
    if not (user_phone_number in get_phones()):
        users.pop(user_id, None)

    # Removing all temporary files
    delete_files_startswith(str(user_id))

    # Reset data
    input_data.pop(user_id, None)
    set_input_data(state, Card(dt=get_now(),
                               user_id=user_id,
                               phone_number=user_phone_number,
                               # protocol='АВ123456',
                               # gn='В062ВВ62',
                               # article='article',
                               # address='address',
                               # parking='parking',
                               # model='model',
                               )
                   )
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


def get_value_card_text(user_data, key, display_value=True):
    value = user_data.get(key, EMPTY) if user_data else EMPTY
    result = get_validate_symbol(value != EMPTY)
    if display_value:
        result += f' {markdown.hitalic(value)}' if value == EMPTY else f'{markdown.hbold(value)}'
    return result


def get_card_text(user_data) -> str:
    text = markdown.text(
        markdown.hbold(f'🚔 КАРТОЧКА НАРУШЕНИЯ {get_validate_symbol(validate_card(user_data))}'),
        markdown.hbold(f'(👮‍♂️ - 📱{user_data.get("phone_number")})'),
        '',
        f'Дата и время: {get_value_card_text(user_data, "dt")}',
        f'Адрес: {get_value_card_text(user_data, "address")}',
        markdown.text(
            f'Номер ТС: {get_value_card_text(user_data, "gn")}. ',
            f'Марка, модель: {get_value_card_text(user_data, "model")}',
        ),
        f'Статья КоАП РФ: {get_value_card_text(user_data, "article")}',
        f'Протокол: {get_value_card_text(user_data, "protocol")}',
        f'Стоянка: {get_value_card_text(user_data, "parking")}',
        markdown.text(
            f'Фото протокола: {get_value_card_text(user_data, "photo_protocol", display_value=False)} ',
            f'Фото ТС: {get_value_card_text(user_data, "photo_tc", display_value=False)}',
        ),
        '',
        sep='\n'
    )
    return text
