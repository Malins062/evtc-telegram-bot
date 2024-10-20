from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from evtc_bot.config.settings import settings
from evtc_bot.db.redis.models import UserData
from evtc_bot.filters.is_datetime import IsTrueDateTime
from evtc_bot.handlers.card.base_handlers import handle_card
from evtc_bot.states.card_states import CardStates, update_user_data
from evtc_bot.validators.card import validate_dt

router = Router(name=__name__)


@router.message(CardStates.dt, F.text, IsTrueDateTime())
async def handle_card_dt(message: types.Message, state: FSMContext, dt: str):
    await state.update_data(dt=True)
    await update_user_data(state.key.user_id, UserData(dt=dt))
    await message.answer(
        text=f"✔ Дата и время задержания ТС изменена на - {markdown.hbold(dt)}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await handle_card(message, state)


@router.message(CardStates.dt, F.text.cast(validate_dt).as_("dt"))
async def handle_card_invalid_interval_dt(message: types.Message, dt: str):
    await message.answer(
        text=markdown.text(
            "⛔ Неверная дата или время задержания ТС!",
            f'Дата и время "{dt}" должна быть в пределах {settings.dt.delta}ч от текущих даты и времени.',
            sep="\n",
        )
    )


@router.message(CardStates.dt)
async def handle_card_invalid_format_dt(message: types.Message):
    await message.reply(
        text=markdown.text(
            "⛔ Неверная дата или время задержания ТС!",
            'Формат поля: ДД.ММ.ГГГГ ЧЧ:ММ (пример - "31.05.2024 12:27") или',
            'ДДММГГГГЧЧММ (пример - "310520241227").',
            sep="\n",
        )
    )
