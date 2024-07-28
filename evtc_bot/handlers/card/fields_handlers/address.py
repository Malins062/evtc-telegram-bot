from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.db.redis.models import UserData
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.states.card_states import CardStates, update_user_data
from evtc_bot.validators.card import validate_address

router = Router(name=__name__)


@router.message(CardStates.address, F.text.cast(validate_address).as_("address"))
async def handle_card_address(message: types.Message, state: FSMContext, address: str):
    await state.update_data(model=True)
    address = "Г.РЯЗАНЬ, " + address
    await update_user_data(state.key.user_id, UserData(address=address))
    await message.answer(
        text=f"✔ Адрес нарушения ТС изменен на - {markdown.hbold(address)}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(CardStates.address)
async def handle_card_invalid_address(message: types.Message):
    await message.reply(
        text=markdown.text(
            "⛔ Ошибочное значения места нарушения ТС!",
            "Длина строки должна быть в диапазоне 2-100 символов!",
            sep="\n",
        )
    )
