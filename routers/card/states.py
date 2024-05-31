from datetime import datetime
from typing import TypedDict

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
    now_dt = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    data: Card = {'dt': now_dt}
    new_state = state
    await new_state.clear()
    await new_state.update_data(data)
    return new_state


def validate_card(data) -> bool:
    return all(data.get(key, False) for key in Card)


# markdown.text(
#     markdown.hbold(f'🚔 КАРТОЧКА НАРУШЕНИЯ (#{message.from_user.id}) 🚔'),
#     '',
#     f'Дата и время: {markdown.hitalic(user_data.get("dt", states.EMPTY))}',
#     f'Номер ТС: {markdown.hitalic(user_data.get("gn", states.EMPTY))}',
#     f'Марка, модель: {markdown.hitalic(user_data.get("model", states.EMPTY))}',
#     f'Адрес: {markdown.hitalic(user_data.get("address", states.EMPTY))}',
#     f'Статья КоАП РФ: {markdown.hitalic(user_data.get("article", states.EMPTY))}',
#     f'Протокол: {markdown.hitalic(user_data.get("protocol", states.EMPTY))}',
#     '',
#     # f'👇 Для работы пользуйтесь кнопками ({MainButtonText.CARD}, {MainButtonText.SEND}, '
#     # f'{MainButtonText.CLEAR}, ) 👇',
#     sep='\n'
# ),


def get_card_text(user_data, user_id) -> str:
    text = markdown.text(
        markdown.hbold(f'🚔 КАРТОЧКА НАРУШЕНИЯ (#{user_id}) '),
        '',
        f'Дата и время: {markdown.hitalic(user_data.get("dt", EMPTY))}',
        f'Номер ТС: {markdown.hitalic(user_data.get("gn", EMPTY))}',
        f'Марка, модель: {markdown.hitalic(user_data.get("model", EMPTY))}',
        f'Адрес: {markdown.hitalic(user_data.get("address", EMPTY))}',
        f'Статья КоАП РФ: {markdown.hitalic(user_data.get("article", EMPTY))}',
        f'Протокол: {markdown.hitalic(user_data.get("protocol", EMPTY))}',
        '',
        sep='\n'
    )
    return text
