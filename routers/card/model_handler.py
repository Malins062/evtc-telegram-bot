from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from validators.card import validate_model
from .card_handler import handle_card
from .states import CardStates

router = Router(name=__name__)


@router.message(CardStates.model, F.text.cast(validate_model).as_('model'))
async def handle_card_gn(message: types.Message, state: FSMContext, model: str):
    await state.update_data(model=model)
    await message.answer(
        text=f'Модель ТС "{markdown.hbold(message.text)}" изменена. 👌',
    )
    await handle_card(message, state)


@router.message(CardStates.model)
async def handle_card_gn(message: types.Message):
    await message.answer(
        text=markdown.text(
            f'⛔ Ошибочный формат модели ТС - "{markdown.hbold(message.text)}"',
            'Модель ТС должна быть в диапазоне 2-25 символов!',
            sep='\n',
        )
    )
