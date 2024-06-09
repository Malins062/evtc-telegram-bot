from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from validators.card import validate_address
from routers.card.base_handler import handle_card
from states.states import CardStates, set_input_data, Card

router = Router(name=__name__)


@router.message(CardStates.address, F.text.cast(validate_address).as_('address'))
async def handle_card_address(message: types.Message, state: FSMContext, address: str):
    await state.update_data(model=True)
    address = 'Г.РЯЗАНЬ, ' + address
    set_input_data(state, Card(address=address))
    await message.answer(
        text=f'✔ Адрес нарушения ТС изменен на - {markdown.hbold(address)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.address)
async def handle_card_invalid_address(message: types.Message):
    await message.reply(
        text=markdown.text(
            '⛔ Ошибочное значения места нарушения ТС!',
            'Длина строки должна быть в диапазоне 2-100 символов!',
            sep='\n',
        )
    )
