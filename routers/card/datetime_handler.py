from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from validators.card import validate_dt
from .card_handler import handle_card
from .states import CardStates

router = Router(name=__name__)


@router.message(CardStates.dt, F.text.cast(validate_dt).as_('dt'))
async def handle_card_gn(message: types.Message, state: FSMContext, dt: str):
    await state.update_data(dt=dt)
    await message.answer(
        text=f'✔ Дата и время задержания ТС изменена - {markdown.hbold(message.text)}',
    )
    await handle_card(message, state)


@router.message(CardStates.gn)
async def handle_card_gn(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Дата и время задержания ТС - "{markdown.hbold(message.text)}"',
            'Длина поля "Дата и время задержания ТС" должна быть 14 символов!',
            'Формат поля: DD.MM.YYYY HH:SS (пример - "31.05.2024 12:27")',
            sep='\n',
        )
    )
