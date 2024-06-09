from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from validators.card import validate_dt
from routers.card.base_handler import handle_card
from states.states import CardStates, Card, set_input_data

router = Router(name=__name__)


@router.message(CardStates.dt, F.text.cast(validate_dt).as_('dt'))
async def handle_card_dt(message: types.Message, state: FSMContext, dt: str):
    await state.update_data(dt=True)
    set_input_data(state, Card(dt=dt))
    await message.answer(
        text=f'✔ Дата и время задержания ТС изменена на - {markdown.hbold(dt)}',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await handle_card(message, state)


@router.message(CardStates.dt)
async def handle_card_invalid_dt(message: types.Message):
    await message.reply(
        text=markdown.text(
            '⛔ Неверная дата или время задержания ТС!',
            'Формат поля: DD.MM.YYYY HH:SS (пример - "31.05.2024 12:27")',
            sep='\n',
        )
    )
