from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from bot.validators.card import validate_gn
from bot.handlers.card.base_handlers import handle_card
from bot.states.card_states import CardStates, Card, set_input_data

router = Router(name=__name__)


@router.message(CardStates.gn, F.text.cast(validate_gn).as_('gn'))
async def handle_card_gn(message: types.Message, state: FSMContext, gn: str):
    await state.update_data(gn=True)
    set_input_data(state, Card(gn=gn))
    await message.answer(
        text=f'✔ Номер ТС изменен на - {markdown.hbold(gn)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.gn)
async def handle_card_invalid_gn(message: types.Message):
    await message.reply(
        text=markdown.text(
            '⛔ Ошибочный формат номера ТС!',
            'Длина номера ТС должна быть в диапазоне 2-9 символов!',
            sep='\n',
        )
    )
