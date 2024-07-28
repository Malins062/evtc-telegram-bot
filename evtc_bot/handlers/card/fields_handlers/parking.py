from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.config.values import parking
from evtc_bot.db.redis.models import UserData
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.states.card_states import CardStates, update_user_data

router = Router(name=__name__)


@router.message(CardStates.parking, F.text.in_(parking))
async def handle_card_parking(message: types.Message, state: FSMContext):
    await state.update_data(parking=True)
    value_parking = parking.get(message.text)
    await update_user_data(state.key.user_id, UserData(parking=value_parking))
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
