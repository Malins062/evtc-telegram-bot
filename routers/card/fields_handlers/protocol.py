from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from validators.card import validate_protocol
from routers.card.card_handler import handle_card
from routers.card.states import CardStates, Card, set_input_data

router = Router(name=__name__)


@router.message(CardStates.protocol, F.text.cast(validate_protocol).as_('protocol'))
async def handle_card_protocol(message: types.Message, state: FSMContext, protocol: str):
    await state.update_data(protocol=True)
    set_input_data(state, Card(protocol=protocol))
    await message.answer(
        text=f'✔ № протокола задержания изменен на - {markdown.hbold(protocol)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.protocol)
async def handle_card_invalid_protocol(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Ошибочный формат номера протокола - "{markdown.hbold(message.text)}"',
            'Длина значения должна быть 10 символов!',
            'Формат значения: 62XXNNNNNN, где X - буква русского алфавита, N - цифра.',
            'Например: 62АВ152522',
            sep='\n',
        )
    )
