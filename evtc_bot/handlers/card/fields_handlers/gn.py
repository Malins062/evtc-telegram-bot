from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.states.card_states import Card, CardStates, set_input_data
from evtc_bot.validators.card import validate_gn

router = Router(name=__name__)


@router.message(CardStates.gn, F.text.cast(validate_gn).as_("gn"))
async def handle_card_gn(message: types.Message, state: FSMContext, gn: str):
    await state.update_data(gn=True)
    set_input_data(state, Card(gn=gn))
    await message.answer(
        text=f"✔ Номер ТС изменен на - {markdown.hbold(gn)}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(CardStates.gn)
async def handle_card_invalid_gn(message: types.Message):
    await message.reply(
        text=markdown.text(
            "⛔ Ошибочный формат номера ТС!",
            "Длина номера ТС должна быть в диапазоне 2-9 символов!",
            sep="\n",
        )
    )
