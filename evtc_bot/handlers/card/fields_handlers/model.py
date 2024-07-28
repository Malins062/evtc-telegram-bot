from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.db.redis.models import UserData
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.states.card_states import CardStates, update_user_data
from evtc_bot.validators.card import validate_model

router = Router(name=__name__)


@router.message(CardStates.model, F.text.cast(validate_model).as_("model"))
async def handle_card_model(message: types.Message, state: FSMContext, model: str):
    await state.update_data(model=True)
    await update_user_data(state.key.user_id, UserData(model=model))
    await message.answer(
        text=f"✔ Модель ТС изменена на - {markdown.hbold(model)}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(CardStates.model)
async def handle_card_invalid_model(message: types.Message):
    await message.reply(
        text=markdown.text(
            "⛔ Ошибочный формат модели ТС!",
            "Модель ТС должна быть в диапазоне 2-25 символов!",
            sep="\n",
        )
    )
