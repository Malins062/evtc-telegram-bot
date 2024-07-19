from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from bot.config.values import parking
from bot.handlers.card.base_handlers import handle_card
from bot.states.card_states import CardStates, set_input_data, Card

router = Router(name=__name__)


@router.message(CardStates.parking, F.text.in_(parking))
async def handle_card_parking(message: types.Message, state: FSMContext):
    await state.update_data(parking=True)
    value_parking = parking.get(message.text)
    set_input_data(state, Card(parking=value_parking))
    await message.answer(
        text=f"✔ Место стоянки, задержанного ТС изменено на - {markdown.hbold(value_parking)}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(CardStates.parking)
async def handle_card_invalid_parking(message: types.Message):
    await message.reply(
        text=markdown.text(
            "⛔ Ошибочное значения стоянки, задержанного ТС!",
            "Выберите штрафную стоянку из предложенного списка 👇",
            sep="\n",
        )
    )
