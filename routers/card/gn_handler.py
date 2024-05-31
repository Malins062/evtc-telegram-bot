from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from validators.card import validate_gn
from .card_handler import handle_card
from .states import CardStates

router = Router(name=__name__)


@router.message(CardStates.gn, F.text.cast(validate_gn).as_('gn'))
async def handle_card_gn(message: types.Message, state: FSMContext, gn: str):
    await state.update_data(gn=gn)
    await message.answer(
        text=f'✔ Номер ТС изменен на - {markdown.hbold(gn)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.gn)
async def handle_card_gn(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Ошибочный формат номера ТС - "{markdown.hbold(message.text)}"',
            'Длина номера ТС должна быть в диапазоне 2-9 символов!',
            sep='\n',
        )
    )
