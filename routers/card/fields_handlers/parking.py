from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from config_data.config import settings
from routers.card.base_handler import handle_card
from states.states import CardStates, set_input_data, Card

router = Router(name=__name__)


@router.message(CardStates.parking, F.text.in_(settings.select_values['parking']))
async def handle_card_parking(message: types.Message, state: FSMContext):
    await state.update_data(parking=True)
    value_parking = settings.select_values['parking'].get(message.text)
    set_input_data(state, Card(parking=value_parking))
    await message.answer(
        text=f'✔ Место стоянки, задержанного ТС изменено на - {markdown.hbold(value_parking)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.parking)
async def handle_card_invalid_parking(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Ошибочное значения стоянки, задержанного ТС - "{markdown.hbold(message.text)}"',
            'Выберите штрафную стоянку из предложенного списка 👇',
            sep='\n',
        )
    )
