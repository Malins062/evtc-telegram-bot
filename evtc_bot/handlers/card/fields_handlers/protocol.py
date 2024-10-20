from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.db.redis.models import UserData
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.states.card_states import CardStates, update_user_data
from evtc_bot.validators.card import validate_protocol

router = Router(name=__name__)


@router.message(CardStates.protocol, F.text.cast(validate_protocol).as_("protocol"))
async def handle_card_protocol(
    message: types.Message, state: FSMContext, protocol: str
):
    await state.update_data(protocol=True)
    await update_user_data(state.key.user_id, UserData(protocol=protocol))
    await message.answer(
        text=f"✔ № протокола задержания изменен на - {markdown.hbold(protocol)}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(CardStates.protocol)
async def handle_card_invalid_protocol(message: types.Message):
    await message.reply(
        text=markdown.text(
            # f'⛔ Ошибочный формат номера протокола - "{markdown.hbold(message.text)}"',
            # 'Длина значения должна быть 10 символов!',
            # 'Например: 62АВ152522',
            "⛔ Ошибочный формат номера протокола!",
            "Формат значения: AANNNNNN, где A - буква русского (2 буквы) алфавита, N - цифра (6 цифр).",
            "Например: АВ152786",
            sep="\n",
        )
    )
